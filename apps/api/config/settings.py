import os
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers
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
JWT_SIGNING_KEY = os.getenv("DJANGO_JWT_SIGNING_KEY")
if not JWT_SIGNING_KEY and IS_LOCAL:
    JWT_SIGNING_KEY = SECRET_KEY
if not JWT_SIGNING_KEY or len(JWT_SIGNING_KEY) < 50:
    raise ImproperlyConfigured("DJANGO_JWT_SIGNING_KEY must contain at least 50 characters.")
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
    "dotick.organization",
    "dotick.items",
    "dotick.tasks",
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
EMAIL_BACKEND = os.getenv("DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL", "no-reply@dotick.local")
GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "")
WEBAUTHN_RP_ID = os.getenv("WEBAUTHN_RP_ID", "localhost" if IS_LOCAL else "")
WEBAUTHN_RP_NAME = os.getenv("WEBAUTHN_RP_NAME", "Dotick")
WEBAUTHN_ORIGINS = os.getenv("WEBAUTHN_ORIGINS", "http://localhost:8081" if IS_LOCAL else "").split(
    ","
)
EMAIL_HOST = os.getenv("DJANGO_EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("DJANGO_EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.getenv("DJANGO_EMAIL_USE_TLS", "1") == "1"
EMAIL_TIMEOUT = 10
CORS_ALLOWED_ORIGINS = os.getenv("DJANGO_CORS_ORIGINS", "http://127.0.0.1:8081").split(",")
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOW_HEADERS = (*default_headers, "if-match")
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
    "DEFAULT_AUTHENTICATION_CLASSES": ["dotick.identity.authentication.SessionJWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": JWT_SIGNING_KEY,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"json": {"()": "config.observability.JsonFormatter"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "json"}},
    "root": {"handlers": ["console"], "level": os.getenv("LOG_LEVEL", "INFO")},
    "loggers": {"django": {"handlers": ["console"], "level": "WARNING", "propagate": False}},
}
