from .base import *
import os

DEBUG = os.getenv("DJANGO_DEBUG") 
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if os.getenv("DJANGO_ALLOWED_HOSTS") else []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST", 'db'),
        'PORT': os.getenv("DB_PORT", 5432)
    }
}