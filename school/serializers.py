import requests
import stripe
from rest_framework import serializers

from school.models import Course, Lesson, Payments, Subscription
from school.validators import LessonLinkValidator


# pro generics takto:
class LessonSerializer(serializers.ModelSerializer):
    # link = serializers.CharField(validators=[LessonLinkValidator("link")])  # tak jak to psal Maslov mi to nejde,
                                                                            # takhle podle chatGPT to jde....
    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {"link": {"validators": [LessonLinkValidator(field='link')]}}  # takhle podle chatGPT to jde....
        # validators = [LessonLinkValidator(field="link")] maslov nefunguje...


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


# pro ViewSet stačí takto:
# je potřeba nainstalovat applikaci Postman >>https://dl.pstmn.io/download/latest/win64<<
# zapnout ji, zapnout django server a do url v applikaci napsat http://localhost:8000/courses/
# pak jde GET, POST, PUT, DELETE atd...
class CourseSerializer(serializers.ModelSerializer):
    # počítat kolik lekcí má jeden course - přidat toto:
    lesson_count = serializers.SerializerMethodField()

    # přidat výstup pro lekce: LessonSerializer hodit nahoru, protože ho tady callujeme
    # pak přidat source, zase díky: related_name="lessons", abych mohl callovat lekce přes Course
    # a many=True, protože Maslov...
    lesson = LessonSerializer(source="lessons", many=True, read_only=True)

    url = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = "__all__"
        title = serializers.CharField(required=False)
        description = serializers.CharField(required=False)
        price = serializers.IntegerField()
        currency = serializers.CharField()

    def get_lesson_count(self, lessons_count):
        # počítat kolik lekcí má jeden course - a pak tady počítám lekce
        # related_name="lessons", abych mohl callovat lekce přes Course
        return lessons_count.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    def get_url(self, obj):
        stripe.api_key = "sk_test_51OeCgjBVY8RAQhG3hJ8Hs8PraP29hbB8lBal33CM3OYWMKkkNXW9dcVHaMtxGmOy4FvZiDwy1ahbbPytfQcSVWsf007kbIKswV"

        # Create a Product on Stripe
        product_data = {
            'name': f'{obj.title}',
            'type': "service",
        }
        response = requests.post('https://api.stripe.com/v1/products', data=product_data,
                                 headers={'Authorization': f'Bearer {stripe.api_key}'})

        product_response = response.json()
        product_id = product_response.get('id')

        # Create a Price for the Product
        price_data = {
            'product': product_id,
            'unit_amount': f"{obj.price}",
            'currency': f'{obj.currency}'
        }
        response = requests.post('https://api.stripe.com/v1/prices', data=price_data,
                                 headers={'Authorization': f'Bearer {stripe.api_key}'})

        price_response = response.json()
        price_id = price_response.get("id")

        # Create a PaymentLink
        payment_link_data = {
            'line_items': [{'price': price_id, 'quantity': 1}]
        }
        payment_link_response = stripe.PaymentLink.create(**payment_link_data)
        return payment_link_response["url"]

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=["user", "course"],
                message="Already Subscribed!"
            )
        ]