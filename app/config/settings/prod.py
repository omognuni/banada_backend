import os

from .base import *

DEBUG = False

#   - DB_HOST=${DB_HOST}
#   - DB_NAME=${DB_NAME}
#   - DB_USER=${DB_USER}
#   - DB_PASS=${DB_PASS}
#   - DB_PORT=5432


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
