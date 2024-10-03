import os

from .base import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

SERVER_HOST = os.environ.get("SERVER_HOST")
LISTEN_PORT = os.environ.get("LISTEN_PORT")

CSRF_TRUSTED_ORIGINS = [
    f"http://{SERVER_HOST}:{LISTEN_PORT}",
    "http://ec2-3-25-64-39.ap-southeast-2.compute.amazonaws.com:8000",
    "http://ec2-3-25-64-39.ap-southeast-2.compute.amazonaws.com",
    os.environ.get("DNS"),
]
