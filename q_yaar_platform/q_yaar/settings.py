"""
Django settings for q_yaar project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import dj_database_url

from decouple import config
from kombu import Queue, Exchange
from pathlib import Path

from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#######################################################################################################################

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

IS_PROD = config("IS_PROD", default=True, cast=bool)
IS_PREPROD = config("IS_PREPROD", default=False, cast=bool) and (not IS_PROD)
IS_LOCAL = config("IS_LOCAL", default=False, cast=bool)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-p(ik-w@g&pzgae#3+h*v57&#trv7jskbmu%w3ha_5v%&qxb8r*"

ALLOWED_HOSTS = []

#######################################################################################################################

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "django_celery_beat",
    "pghistory",  # Django audit trail
    "pgtrigger",  # Django audit trail - trigger
    "pgconnection",  # Django audit trail - connection
    "rest_framework_simplejwt",  # Django Simple JWT
]

PROJECT_APPS = [
    "account.apps.AccountConfig",
    "profile_player.apps.ProfilePlayerConfig",
    "jwt_auth.apps.JwtAuthConfig",
    "treasure_hunt.apps.TreasureHuntConfig",
    "game_history.apps.GameHistoryConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "log_request_id.middleware.RequestIDMiddleware",  # Logging-Request-ID
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "q_yaar.urls"

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
            ]
        },
    }
]

WSGI_APPLICATION = "q_yaar.wsgi.application"

#######################################################################################################################

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASE_URL = config("DATABASE_URL")

DEFAULT_DB_CONFIG = dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=not DEBUG)

# For running UTs
DEFAULT_DB_CONFIG["TEST"] = {"NAME": config("TEST_DB_NAME")}

DATABASES = {
    "default": {
        "ENGINE": DEFAULT_DB_CONFIG["ENGINE"],
        "NAME": DEFAULT_DB_CONFIG["NAME"],
        "USER": DEFAULT_DB_CONFIG["USER"],
        "PASSWORD": DEFAULT_DB_CONFIG["PASSWORD"],
        "HOST": DEFAULT_DB_CONFIG["HOST"],
        "PORT": DEFAULT_DB_CONFIG["PORT"],
        "CONN_MAX_AGE": DEFAULT_DB_CONFIG["CONN_MAX_AGE"],
        "TEST": {"NAME": DEFAULT_DB_CONFIG["TEST"]["NAME"]},
    }
}

#######################################################################################################################

# Cache

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "qyaar.api",
    }
}

LAST_LOGIN_CACHE_TTL = 24 * 60 * 60  # (24 hours)

#######################################################################################################################

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "account.PlatformUser"

#######################################################################################################################

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

#######################################################################################################################

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

#######################################################################################################################

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#######################################################################################################################

# Django REST Framework

REST_FRAMEWORK = {
    "PAGE_SIZE": 20,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": config("ANON_THROTTLING", default="4000/minute"),
        "user": config("USER_THROTTLING", default="100000000/minute"),
        "token-less-url": config("TOKEN_LESS_THROTTLING", default="100/minute"),
        "token-less-auth-url-burst": config("TOKEN_LESS_AUTH_THROTTLING_BURST", default="100/minute"),
        "token-less-auth-url-sustained": config("TOKEN_LESS_AUTH_THROTTLING_SUSTAINED", default="10000/day"),
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

#######################################################################################################################

# Celery

CELERY_QUEUES = (
    # Slow Queues
    Queue("default", Exchange("default"), routing_key="default"),
    # Fast Queues
    Queue("example", Exchange("example"), routing_key="example"),
)

CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "default"
CELERY_DEFAULT_ROUTING_KEY = "default"

CELERY_BROKER_URL = config("REDIS_URL")
# Enable this, along with celerybackend in 3rd party apps if required
CELERY_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERYD_TASK_SOFT_TIME_LIMIT = 60
if IS_LOCAL and DEBUG:  # For local and unit tests
    CELERY_TASK_ALWAYS_EAGER = True

if IS_PREPROD:
    CELERY_REDIS_MAX_CONNECTIONS = 30
    BROKER_POOL_LIMIT = 15
else:
    CELERY_REDIS_MAX_CONNECTIONS = 50
    BROKER_POOL_LIMIT = 20

BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 86400}  # 1 day
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

#######################################################################################################################

# Logger

APPLICATION_LOGGERS_DEFAULT_LEVEL = "DEBUG"
APPLICATION_LOGGERS_DEFAULT_HANDLERS = ["console"]

APPLICATION_LOGGERS = {
    "account": {
        "handlers": APPLICATION_LOGGERS_DEFAULT_HANDLERS,
        "level": APPLICATION_LOGGERS_DEFAULT_LEVEL,
        "propagate": False,
    },
    "jwt_auth": {
        "handlers": APPLICATION_LOGGERS_DEFAULT_HANDLERS,
        "level": APPLICATION_LOGGERS_DEFAULT_LEVEL,
        "propagate": False,
    },
    "profile_player": {
        "handlers": APPLICATION_LOGGERS_DEFAULT_HANDLERS,
        "level": APPLICATION_LOGGERS_DEFAULT_LEVEL,
        "propagate": False,
    },
    "treasure_hunt": {
        "handlers": APPLICATION_LOGGERS_DEFAULT_HANDLERS,
        "level": APPLICATION_LOGGERS_DEFAULT_LEVEL,
        "propagate": False,
    },
    "game_history": {
        "handlers": APPLICATION_LOGGERS_DEFAULT_HANDLERS,
        "level": APPLICATION_LOGGERS_DEFAULT_LEVEL,
        "propagate": False,
    },
}

DJANGO_DEFAULT_LOGGERS = {
    "django": {"handlers": (["console"]), "propagate": False, "level": "ERROR" if IS_PROD else "INFO"},
    "django.request": {"handlers": (["console"]), "level": "ERROR", "propagate": False},
    "django.db": {"handlers": (["console"]), "propagate": False, "level": "ERROR" if IS_PROD else "WARNING"},
    "django.security": {"handlers": (["console"]), "propagate": False, "level": "WARNING" if IS_PROD else "DEBUG"},
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {request_id} {name} {funcName} {lineno} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {"format": "{levelname} {message}", "style": "{"},
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "request_id": {"()": "log_request_id.filters.RequestIDFilter"},
    },
    "handlers": {
        "null": {"class": "logging.NullHandler"},
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["request_id"],
        },
    },
    "loggers": {**DJANGO_DEFAULT_LOGGERS, **APPLICATION_LOGGERS},
}

#######################################################################################################################

# Game Config
GAME_CODE_LENGTH = config("GAME_CODE_LENGTH", cast=int, default=6)
