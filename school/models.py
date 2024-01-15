from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=64, verbose_name="Course title")
    preview = models.ImageField(upload_to="course/", verbose_name="Course preview", null=True, blank=True)
    description = models.TextField(max_length=1024, verbose_name="Description")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Lesson(models.Model):
    title = models.CharField(max_length=64, verbose_name="Lesson title")
    description = models.TextField(max_length=1024, verbose_name="Description")
    preview = models.ImageField(upload_to="lesson/", verbose_name="Lesson preview", null=True, blank=True)
    link = models.CharField(max_length=64, verbose_name="Lesson link")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
