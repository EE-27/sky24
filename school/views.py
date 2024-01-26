from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from school.models import Course, Lesson, Payments, Subscription
from school.permissions import IsModerator, IsOwner
from school.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer


# pro ViewSet stačí takto:
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [
        IsAdminUser | IsModerator | IsOwner]  # když dám [IsModerator] tak tam může jen harry potter - group:moderaator
    # permission_classes = [IsAuthenticated]  # takhle se zamnkne, teď /courses/ může vidět jen s Acces_token


# pro generics takto:
class LessonCreateAPIView(generics.CreateAPIView):  # POST
    serializer_class = LessonSerializer
    # neni potřeba queryset
    permission_classes = [IsAuthenticated]


class LessonListAPIView(generics.ListAPIView):  # GET
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]


class LessonRetrieveAPIView(generics.RetrieveAPIView):  # GET
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser | IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):  # PATCH (může být 1 field)
    serializer_class = LessonSerializer  # PUT (chce všechno)
    queryset = Lesson.objects.all()
    permission_classes = [IsAdminUser | IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):  # DELETE
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()  # Maslov ve videu o Generics tenhle řádek nemá,
    permission_classes = [IsAuthenticated]  # mně to nešlo bez něj ¯\_(ツ)_/¯


class PaymentsListAPIView(generics.ListAPIView):
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
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

class SubscribeToCourse(APIView):
    def post(self, request, course_id):
        user = request.user
        course = Course.objects.get(id=course_id)

        # Check if the subscription already exists
        if not Subscription.objects.filter(user=user, course=course).exists():
            Subscription.objects.create(user=user, course=course)
            return Response({'message': 'Subscribed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Already subscribed'}, status=status.HTTP_400_BAD_REQUEST)

class UnsubscribeFromCourse(APIView):
    def post(self, request, course_id):
        user = request.user
        course = Course.objects.get(id=course_id)

        # Check if the subscription exists
        subscription = Subscription.objects.filter(user=user, course=course).first()
        if subscription:
            subscription.delete()
            return Response({'message': 'Unsubscribed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Not subscribed'}, status=status.HTTP_400_BAD_REQUEST)