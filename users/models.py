from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Díky tomuhle modelu se musí udělat users/management/commands - csu.py,
    protože createsuperuser chce username a ne email.
    """
    phone_number = models.CharField(max_length=16, verbose_name="Phone",null=True, blank=True)
    city = models.CharField(max_length=64, verbose_name="City",null=True, blank=True)
    avatar = models.ImageField(upload_to="users/", verbose_name="Avatar", null=True, blank=True)

    username = None
    email = models.EmailField(unique=True, verbose_name="Mail")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
