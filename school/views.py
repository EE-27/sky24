import requests
import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from school.models import Course, Lesson, Payments, Subscription
from school.pagination import LessonPagination, CoursePagination
from school.permissions import IsModerator, IsOwner
from school.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer


# pro ViewSet stačí takto:
class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet for Courses
    GET /courses/
    POST /courses/
    GET /courses/{id}/
    PUT /courses/{id}/
    PATCH /courses/{id}/
    DELETE /courses/{id}/
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # pagination_class = CoursePagination  # na testy vypnout
    permission_classes = [AllowAny]  # [
    #  IsAdminUser | IsModerator | IsOwner]  # když dám [IsModerator] tak tam může jen harry potter - group:moderaator
    # permission_classes = [IsAuthenticated]  # takhle se zamnkne, teď /courses/ může vidět jen s Acces_token


# pro generics takto:
class LessonCreateAPIView(generics.CreateAPIView):  # POST
    """ Generics for Lesson
    POST /lesson/create/
    """
    serializer_class = LessonSerializer
    # neni potřeba queryset
    permission_classes = [AllowAny]


class LessonListAPIView(generics.ListAPIView):  # GET
    """ Generics for Lesson
    GET /lesson/
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPagination
    permission_classes = [AllowAny]


class LessonRetrieveAPIView(generics.RetrieveAPIView):  # GET
    """ Generics for Lesson
    GET /lesson/{id}/
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]  # [IsAdminUser | IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):  # PATCH (může být 1 field)
    """ Generics for Lesson
    PUT /lesson/update/{id}/
    PATCH /lesson/update/{id}/
    """
    serializer_class = LessonSerializer  # PUT (chce všechno)
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]  # [IsAdminUser | IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):  # DELETE
    """ Generics for Lesson
    DELETE /lesson/delete/{id}/
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()  # Maslov ve videu o Generics tenhle řádek nemá,
    permission_classes = [AllowAny]  # [IsAuthenticated]  # mně to nešlo bez něj ¯\_(ツ)_/¯


class PaymentsListAPIView(generics.ListAPIView):
    """ Generics for Payments
    GET /payments/
    """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    # bacha import musí být z těchto:
    # from django_filters.rest_framework import DjangoFilterBackend
    # from rest_framework.filters import SearchFilter, OrderingFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["course_or_lesson", "payment_method"]
    search_fields = ["course_or_lesson", "payment_method"]
    ordering_fields = ["payment_date"]
    # http://localhost:8000/payments/?payment_method=transfer --- jenom transfer
    # http://localhost:8000/payments/?course_or_lesson=lesson --- jenom lekce
    # http://localhost:8000/payments/?ordering=payment_date --- podle data


class PaymentsUpdateAPIView(generics.UpdateAPIView):
    """ Generics for Payments
    PUT payments/update/{id}/
    PATCH payments/update/{id}/
    """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    """ Generics for Payments
    GET /payments/{id}/
    """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


# class SubscribeToCourse(APIView):
#     def post(self, request, course_id):
#         user = request.user
#         course = Course.objects.get(id=course_id)
#
#         # Check if the subscription already exists
#         if not Subscription.objects.filter(user=user, course=course).exists():
#             Subscription.objects.create(user=user, course=course)
#             return Response({'message': 'Subscribed successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'Already subscribed'}, status=status.HTTP_400_BAD_REQUEST)
#
# class UnsubscribeFromCourse(APIView):
#     def post(self, request, course_id):
#         user = request.user
#         course = Course.objects.get(id=course_id)
#
#         # Check if the subscription exists
#         subscription = Subscription.objects.filter(user=user, course=course).first()
#         if subscription:
#             subscription.delete()
#             return Response({'message': 'Unsubscribed successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'message': 'Not subscribed'}, status=status.HTTP_400_BAD_REQUEST)

class SubscriptionCreateAPIview(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class SubscriptionUpdateAPIview(generics.UpdateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionDestroyAPIview(generics.DestroyAPIView):
    queryset = Subscription.objects.all()


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class CoursePaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSerializer

class CoursePaymentListAPIView(generics.ListAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


    # def payment_create(self, request):
    #     stripe.api_key = "sk_test_51OeCgjBVY8RAQhG3hJ8Hs8PraP29hbB8lBal33CM3OYWMKkkNXW9dcVHaMtxGmOy4FvZiDwy1ahbbPytfQcSVWsf007kbIKswV"
    #
    #     # Create a Product on Stripe
    #     product_data = {
    #         'name': 'Starter Setup',  # Adjust the name as needed
    #         'type':"service",
    #     }
    #     response = requests.post('https://api.stripe.com/v1/products', data=product_data,
    #                              headers={'Authorization': f'Bearer {stripe.api_key}'})
    #
    #     # Check if the product creation was successful
    #     if response.status_code != 200:
    #         return Response({'error': f'Failed to create product on Stripe: {response.text}'},
    #                         status=response.status_code)
    #
    #
    #     product_response = response.json()
    #     product_id = product_response.get('id')
    #
    #     # Create a Price for the Product
    #     price_data = {
    #         'product': product_id,
    #         'unit_amount': 2000,
    #         'currency': 'usd'
    #     }
    #     response = requests.post('https://api.stripe.com/v1/prices', data=price_data,
    #                              headers={'Authorization': f'Bearer {stripe.api_key}'})
    #
    #     # Check if the price creation was successful
    #     if response.status_code != 200:
    #         return Response({'error': f'Failed to create price on Stripe: {response.text}'},
    #                         status=response.status_code)
    #
    #
    #     price_response = response.json()
    #     price_id = price_response.get("id")
    #
    #
    #     # Create a PaymentLink
    #     payment_link_data = {
    #         'line_items': [{'price': price_id, 'quantity': 1}]
    #     }
    #     payment_link_response = stripe.PaymentLink.create(**payment_link_data)
    #     print(payment_link_response["url"])
    #     return Response({'payment_link_url': payment_link_response.url}, status=status.HTTP_200_OK)

        # product = stripe.Product.create(
        #     name=f"{Course.title}",
        #     default_price_data={"unit_amount": Course.price, "currency": "usd"},
        #     expand=["default_price"],
        # )
        #
        # data = {'name': f"{Course.title}", "default_price_data":{"unit_amount": Course.price, "currency": "usd"}, 'expand': ["default_price"]}
        # response = self.client.post('v1/products/', data)
        # price = stripe.Price.create(
        #     product=product,
        #     unit_amount=Course.price,
        #     currency="czk",
        #     recurring={"interval": "month"},
        # )
        # payment_link = stripe.PaymentLink.create(
        #     line_items=[{"price": price, "quantity": 1}],
        # )
        #
        # # You can create a new course instance or update an existing one here
        # # For demonstration purposes, assuming you have a Course model
        # course_data = {
        #     "title": "Your Course Title",
        #     "description": "Your Course Description",
        #     "amount": 1991,  # Adjust the amount based on your use case
        #     "currency": "usd",
        #     # Add other course fields as needed
        # }
        #
        # # Assuming you have a Course model, create or update the course
        # course_serializer = CourseSerializer(data=course_data)
        # if course_serializer.is_valid():
        #     course_instance = course_serializer.save()
        #     return Response({
        #         'course': course_serializer.data,
        #         'payment_link_url': payment_link.url
        #     }, status=status.HTTP_200_OK)