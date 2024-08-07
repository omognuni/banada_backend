import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-yfr2(g3b#on@_cieci2qtiwe4$dn5911(&mj4v2x1h-ay*y#0o"
)

DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # OAuth2
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.kakao",
    "allauth.socialaccount.providers.instagram",
    # DRF
    "rest_framework",
    "drf_spectacular",
    # APP
    "core",
    "profile",
    "user",
    "contact",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "config.middleware.JsonContentTypeMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# OAuth2
SITE_ID = 1

AUTHENTICATION_BACKENDS = ("allauth.account.auth_backends.AuthenticationBackend",)

LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login/"
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    "kakao": {
        "APP": {
            "client_id": os.environ.get("KAKAO_CLIENT_ID", ""),
            "secret": os.environ.get("KAKAO_SECRET", ""),
            "key": os.environ.get("KAKAO_KEY", ""),
        }
    },
    "instagram": {
        "APP": {
            "client_id": os.environ.get("INSTAGRAM_CLIENT_ID", ""),
            "secret": os.environ.get("INSTAGRAM_SECRET", ""),
            "key": os.environ.get("INSTAGRAM_KEY", ""),
        }
    },
}

SPECTACULAR_SETTINGS = {
    # General schema metadata. Refer to spec for valid inputs
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#openapi-object
    "TITLE": "Banada",
    "DESCRIPTION": "",
    # Optional: MAY contain "name", "url", "email"
    "SWAGGER_UI_SETTINGS": {
        # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/  <- 여기 들어가면 어떤 옵션들이 더 있는지 알수있습니다.
        "dom_id": "#swagger-ui",  # required(default)
        "layout": "BaseLayout",  # required(default)
        # API를 클릭할때 마다 SwaggerUI의 url이 변경됩니다. (특정 API url 공유시 유용하기때문에 True설정을 사용합니다)
        "deepLinking": True,
        # True 이면 SwaggerUI상 Authorize에 입력된 정보가 새로고침을 하더라도 초기화되지 않습니다.
        "persistAuthorization": True,
        # True이면 API의 urlId 값을 노출합니다. 대체로 DRF api name둘과 일치하기때문에 api를 찾을때 유용합니다.
        "displayOperationId": True,
        "filter": True,  # True 이면 Swagger UI에서 'Filter by Tag' 검색이 가능합니다
    },
    # Optional: MUST contain "name", MAY contain URL
    "VERSION": "2.0.0",
    "SERVE_INCLUDE_SCHEMA": False,  # OAS3 Meta정보 API를 비노출 처리합니다.
    # Swagger UI 버전을 조절할수 있습니다.
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@3.38.0",
    "COMPONENT_SPLIT_REQUEST": True,
    "DISABLE_ERRORS_AND_WARNINGS": True,
}
