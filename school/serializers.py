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

    is_subscribed = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, lessons_count):
        # počítat kolik lekcí má jeden course - a pak tady počítám lekce
        # related_name="lessons", abych mohl callovat lekce přes Course
        return lessons_count.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'