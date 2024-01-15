from rest_framework import viewsets, generics

from school.models import Course, Lesson
from school.serializers import CourseSerializer, LessonSerializer


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
