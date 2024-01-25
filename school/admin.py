from django.contrib import admin

from school.models import Course, Lesson, Payments


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "description")

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "description")

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ("user", "course_or_lesson", "payment_date")
