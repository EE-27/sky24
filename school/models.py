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
    link = models.CharField(max_length=64, verbose_name="Lesson link", null=True, blank=True)
    # počítat kolik lekcí má jeden course: bylo nutný spojit model Lesson s modelem Course
    # v Postman při přidávání lekce: "course" : 3, related_name= abych mohl callovat lekce přes Course
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"


class Payments(models.Model):
    # zapsáno do modolu pomocí "fixtur tool", to znaméná: vytvořen .json a potom: python manage.py loaddata payments
    # formát pro json:
    # [
    #     {
    #         "model": "school.payments", \\ jméno app a jméno modelu
    #         "pk": 1, \\ vždy změnit, jinak se jenom přepisuje
    #         "fields": {
    #             "user": "Honza",
    #             "payment_date": "2024-01-18", \\ YYYY-MM-DD
    #             "course_or_lesson": "course", \\ "course" nebo "lesson"
    #             "payment_amount": 500,
    #             "payment_method": "cash" \\ "cash" nebo "transfer"
    #         }
    #     }
    # ]

    COURSE_OR_LESSON = [
        ("course", "Course"),
        ("lesson", "Lesson")
    ]
    PAYMENT_METHOD = [
        ("cash", "Cash"),
        ("transfer", "Transfer")
    ]
    user = models.CharField(max_length=24, verbose_name="User")
    payment_date = models.DateField(verbose_name="Payment date")
    course_or_lesson = models.CharField(max_length=12, verbose_name="Paid course or lesson?", choices=COURSE_OR_LESSON,
                                        null=True, blank=True)
    payment_amount = models.IntegerField(verbose_name="Payment amount")
    payment_method = models.CharField(max_length=12, verbose_name="Payment method", choices=PAYMENT_METHOD, null=True,
                                      blank=True)

    def __str__(self):
        return f"{self.user} - method: {self.payment_method} - amount: {self.payment_amount}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
