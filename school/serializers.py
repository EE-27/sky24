from rest_framework import serializers

from school.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
# pro ViewSet stačí takto:
# je potřeba nainstalovat applikaci Postman >>https://dl.pstmn.io/download/latest/win64<<
# zapnout ji, zapnout django server a do url v applikaci napsat http://localhost:8000/courses/
# pak jde GET, POST, PUT, DELETE atd...
