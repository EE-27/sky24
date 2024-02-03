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
from school.tasks import process_payment


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


class PaymentsCreateAPIView(generics.CreateAPIView):  # POST
    """ Generics for Payments
    POST /payments/create/
    """
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        new_payment = serializer.save()
        process_payment.delay(new_payment.id)


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