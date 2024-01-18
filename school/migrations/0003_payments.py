# Generated by Django 5.0.1 on 2024-01-18 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_lesson_course_alter_lesson_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=24, verbose_name='User')),
                ('payment_date', models.DateField(verbose_name='Payment date')),
                ('course_or_lesson', models.CharField(blank=True, choices=[('course', 'Course'), ('lesson', 'Lesson')], max_length=12, null=True, verbose_name='Paid course or lesson?')),
                ('payment_amount', models.IntegerField(verbose_name='Payment amount')),
                ('payment_method', models.CharField(blank=True, choices=[('cash', 'Cash'), ('transfer', 'Transfer')], max_length=12, null=True, verbose_name='Payment method')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
