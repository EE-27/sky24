# Generated by Django 5.0.1 on 2024-01-25 13:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_payments'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lesson',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='payments',
            name='user',
            field=models.CharField(blank=True, max_length=24, null=True, verbose_name='User'),
        ),
    ]
