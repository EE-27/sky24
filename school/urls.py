from django.urls import path

from school.apps import SchoolConfig
from rest_framework.routers import DefaultRouter

from school.views import (CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView,
                          LessonUpdateAPIView, LessonDestroyAPIView, PaymentsListAPIView)

app_name = SchoolConfig.name

router = DefaultRouter()  # pro ViewSet stačí takto: router a prázdný urls + dole router.urls
router.register(r"courses", CourseViewSet, basename="courses")
urlpatterns = [
    # pro generics CRUD:
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list "),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_get "),
    path("lesson/update/<int:pk>/",LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/delete/<int:pk>/",LessonDestroyAPIView.as_view(), name="lesson_delete"),

    # Payments pro filtry
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list "),
] + router.urls
