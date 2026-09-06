import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / ".env")

ENVIRONMENT = os.getenv("DOTICK_ENV", "production")
IS_LOCAL = ENVIRONMENT in {"local", "test"}
DEBUG = IS_LOCAL and os.getenv("DJANGO_DEBUG", "0") == "1"
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
if len(SECRET_KEY) < 50:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must contain at least 50 characters.")
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
ROOT_URLCONF = "config.urls"
ASGI_APPLICATION = "config.asgi.application"
FOUNDATION_ENABLED = os.getenv("DOTICK_FOUNDATION_ENABLED", "0") == "1"
if FOUNDATION_ENABLED and not IS_LOCAL:
    raise ImproperlyConfigured("The foundation workbench is only available in local/test.")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "rest_framework",
    "corsheaders",
    "dotick.identity",
    "dotick.foundation",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "config.observability.RequestLoggingMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("PGDATABASE", "dotick_dev"),
        "USER": os.environ["PGUSER"],
        "PASSWORD": os.getenv("PGPASSWORD", ""),
        "HOST": os.getenv("PGHOST", "127.0.0.1"),
        "PORT": os.getenv("PGPORT", "5432"),
        "CONN_MAX_AGE": 0,
        "OPTIONS": {"connect_timeout": 3},
    }
}
AUTH_USER_MODEL = "identity.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
USE_TZ = True
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
CORS_ALLOWED_ORIGINS = os.getenv("DJANGO_CORS_ORIGINS", "http://127.0.0.1:8081").split(",")
CORS_ALLOW_CREDENTIALS = False
DATA_UPLOAD_MAX_MEMORY_SIZE = 16_384
SECURE_SSL_REDIRECT = not IS_LOCAL
SESSION_COOKIE_SECURE = not IS_LOCAL
CSRF_COOKIE_SECURE = not IS_LOCAL
SECURE_HSTS_SECONDS = 0 if IS_LOCAL else 31_536_000
SECURE_HSTS_INCLUDE_SUBDOMAINS = not IS_LOCAL
SECURE_HSTS_PRELOAD = not IS_LOCAL
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "config.errors.api_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"json": {"()": "config.observability.JsonFormatter"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "json"}},
    "root": {"handlers": ["console"], "level": os.getenv("LOG_LEVEL", "INFO")},
    "loggers": {"django": {"handlers": ["console"], "level": "WARNING", "propagate": False}},
}
