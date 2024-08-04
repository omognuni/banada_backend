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
LISTEN_PORT = os.environget("LISTEN_PORT")

CSRF_TRUSTED_ORIGINS = [f"http://{SERVER_HOST}:{LISTEN_PORT}"]
