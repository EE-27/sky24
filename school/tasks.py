from celery import shared_task

from school.models import Payments


@shared_task
def process_payment(payment_id):

    payment = Payments.objects.get(pk=payment_id)

    if payment.course_or_lesson == "course":
        print(f"Processing payment for course: {payment.payment_amount} {payment.payment_method}")

    elif payment.course_or_lesson == "lesson":
        print(f"Processing payment for lesson: {payment.payment_amount} {payment.payment_method}")

    else:
        print("Invalid course_or_lesson value")
