"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'django-insecure-_t3_e(kbkei2wxp-n(0&5p74w!5uiz5-ryd23=77ea40#0w=h4'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "rest_framework",
    "drf_yasg",
    "django_celery_beat",

    "users",
    "school",

    "django_filters",  # pip3 install django-filter
    "rest_framework_simplejwt",  # pip3 install djangorestframework-simplejwt
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "sky24",
        "USER": os.getenv("USER_DB"),
        "PASSWORD": os.getenv("USER_PW"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        "rest_framework.permissions.AllowAny"
        # AllowAny - teď to pustí všechny

        # 'rest_framework.permissions.IsAuthenticated',
    ]  # v Postman, teď všechno chce: v Headers napsat: Authorization: Bearer <<access_token>> z /users/api/token/
}

CACHE_ENABLED = True

if CACHE_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/",  # nezapomenout si zpustit redis-server
        }
    }

# Settings for Celery

# # URL of the message broker
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/'  # For example, Redis, which runs on port 6379 by default
#
# # URL of the results broker, also Redis
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
#
# # Time zone for Celery operation
# CELERY_TIMEZONE = "Europe/Prague"
#
# # Task tracking flag
# CELERY_TASK_TRACK_STARTED = True


CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'fuckup@oscarbot.ru'
EMAIL_HOST_PASSWORD = 'AsTSNVv7pun9'
EMAIL_USE_SSL = True

# Nastavení pro Celer
CELERY_BEAT_SCHEDULE = {
    "print-hello-world": {
        "task": 'school.tasks.print_hello_world',
        'schedule': 1.0,
    },
    # 'check_last_login': {
    #     'task': 'school.tasks.check_last_login',  # Cesta k úkolu
    #     'schedule': datetime.timedelta(seconds=1),  # Plán provádění úloh (např. jednou denně)
    # },
}
