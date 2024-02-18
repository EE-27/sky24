from celery import shared_task

from datetime import timedelta

from celery.schedules import crontab
from django.utils import timezone

from school.models import Payments
from users.models import User

from celery import Celery
import time

app = Celery('school', broker='redis://localhost:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def print_hello_world():
    print("Hello, World!")

app.conf.beat_schedule = {
    'print-hello-world-every-minute': {
        'task': 'school.tasks.print_hello_world',
        'schedule': crontab(minute="*/1"),
    },
}


# @shared_task
# def process_payment(payment_id):
#
#     payment = Payments.objects.get(pk=payment_id)
#
#     if payment.course_or_lesson == "course":
#         print(f"Processing payment for course: {payment.payment_amount} {payment.payment_method}")
#
#     elif payment.course_or_lesson == "lesson":
#         print(f"Processing payment for lesson: {payment.payment_amount} {payment.payment_method}")
#
#     else:
#         print("Invalid course_or_lesson value")
#
#
# @shared_task
# def check_last_login():
#     """Úloha na pozadí, která kontroluje uživatele podle data posledního přihlášení v poli last_login."""
#     today = timezone.now()
#     thirty_days_ago = today - timedelta(days=30)
#     for user in User.objects.all():
#         print(user.email)
#         if user.last_login < thirty_days_ago:
#             user.is_active = False
#             print("Změnil uživatele na neaktivního.")
#             user.save()


# celery -A config worker --pool=solo -l info -n worker2@%h
# celery -A config worker -l INFO -P eventlet
# celery -A config worker -l INFO -P gevent