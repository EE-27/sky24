from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email="Stázka@123.com",  # harry_potter@seznam.cz ,  dutch@gay.cz
            first_name="Stázka",
            last_name="Blabla",
            is_staff=True,
            is_superuser=False
        )
        user.set_password("12345")
        user.save()