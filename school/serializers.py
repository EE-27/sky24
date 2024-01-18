from rest_framework import serializers

from school.models import Course, Lesson

# pro generics takto:
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
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
    lesson = LessonSerializer(source="lessons", many=True)

    class Meta:
        model = Course
        fields = "__all__"
    def get_lesson_count(self, lessons_count):
        # počítat kolik lekcí má jeden course - a pak tady počítám lekce
        # related_name="lessons", abych mohl callovat lekce přes Course
        return lessons_count.lessons.count()



