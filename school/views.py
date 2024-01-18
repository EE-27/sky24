from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter

from school.models import Course, Lesson, Payments
from school.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer


# pro ViewSet stačí takto:
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


# pro generics takto:
class LessonCreateAPIView(generics.CreateAPIView):  # POST
    serializer_class = LessonSerializer
    # neni potřeba queryset


class LessonListAPIView(generics.ListAPIView):  # GET
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):  # GET
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):  # PATCH (může být 1 field)
    serializer_class = LessonSerializer             # PUT (chce všechno)
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):  # DELETE
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()  # Maslov ve videu o Generics tenhle řádek nemá,
                                     # mně to nešlo bez něj ¯\_(ツ)_/¯


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