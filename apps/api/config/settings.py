"""
Django settings for the Dotick API foundation.
"""

import os
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = BASE_DIR.parent.parent
load_dotenv(REPO_ROOT / ".env")

DOTICK_ENV = os.getenv("DOTICK_ENV", "local").strip().lower()
IS_LOCAL = DOTICK_ENV in {"local", "test"}


def _env_bool(name, *, default=False):
    raw_value = os.getenv(name)
    if raw_value is None or not raw_value.strip():
        return default

    value = raw_value.strip().lower()
    if value in {"1", "true", "yes", "on"}:
        return True
    if value in {"0", "false", "no", "off"}:
        return False
    raise ImproperlyConfigured(f"{name} must be a boolean value.")


def _env_port(name, *, default):
    raw_value = os.getenv(name)
    if raw_value is None or not raw_value.strip():
        return default
    try:
        port = int(raw_value)
    except ValueError as error:
        raise ImproperlyConfigured(f"{name} must be an integer port.") from error
    if not 1 <= port <= 65_535:
        raise ImproperlyConfigured(f"{name} must be between 1 and 65535.")
    return port


SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = IS_LOCAL and os.getenv("DJANGO_DEBUG", "0") == "1"
ALLOWED_HOSTS = [
    host.strip() for host in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if host.strip()
]
if "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must be an explicit allowlist.")
if not IS_LOCAL and not ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS is required outside local/test.")

default_trusted_origins = "http://127.0.0.1:8081,http://localhost:8081" if IS_LOCAL else ""
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        default_trusted_origins,
    ).split(",")
    if origin.strip()
]
if not IS_LOCAL and not CSRF_TRUSTED_ORIGINS:
    raise ImproperlyConfigured("DJANGO_CSRF_TRUSTED_ORIGINS is required outside local/test.")
if not IS_LOCAL and any(not origin.startswith("https://") for origin in CSRF_TRUSTED_ORIGINS):
    raise ImproperlyConfigured("Production trusted origins must use HTTPS.")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "dotick.identity.apps.IdentityConfig",
    "dotick.organization.apps.OrganizationConfig",
    "dotick.items.apps.ItemsConfig",
    "dotick.tasks.apps.TasksConfig",
    "dotick.foundation.apps.FoundationConfig",
]

AUTH_USER_MODEL = "identity.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "config.middleware.RequestIDMiddleware",
    "config.observability.RequestLoggingMiddleware",
    "config.middleware.JsonRequestBoundaryMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["PGDATABASE"],
        "USER": os.environ["PGUSER"],
        "PASSWORD": os.environ["PGPASSWORD"],
        "HOST": os.environ["PGHOST"],
        "PORT": os.environ["PGPORT"],
        "CONN_MAX_AGE": 0,
        "OPTIONS": {"connect_timeout": 2},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SMTP_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_BACKEND = os.getenv("DJANGO_EMAIL_BACKEND", SMTP_EMAIL_BACKEND).strip()
if not EMAIL_BACKEND:
    raise ImproperlyConfigured("DJANGO_EMAIL_BACKEND may not be blank.")
EMAIL_HOST = os.getenv("DJANGO_EMAIL_HOST", "localhost" if IS_LOCAL else "").strip()
EMAIL_PORT = _env_port("DJANGO_EMAIL_PORT", default=25)
EMAIL_HOST_USER = os.getenv("DJANGO_EMAIL_HOST_USER", "").strip()
EMAIL_HOST_PASSWORD = os.getenv("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = _env_bool("DJANGO_EMAIL_USE_TLS")
EMAIL_USE_SSL = _env_bool("DJANGO_EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = os.getenv(
    "DJANGO_DEFAULT_FROM_EMAIL",
    "webmaster@localhost" if IS_LOCAL else "",
).strip()
if EMAIL_USE_TLS and EMAIL_USE_SSL:
    raise ImproperlyConfigured(
        "DJANGO_EMAIL_USE_TLS and DJANGO_EMAIL_USE_SSL are mutually exclusive."
    )
if bool(EMAIL_HOST_USER) != bool(EMAIL_HOST_PASSWORD):
    raise ImproperlyConfigured(
        "DJANGO_EMAIL_HOST_USER and DJANGO_EMAIL_HOST_PASSWORD must be configured together."
    )
if EMAIL_BACKEND == SMTP_EMAIL_BACKEND and EMAIL_HOST and not DEFAULT_FROM_EMAIL:
    raise ImproperlyConfigured(
        "DJANGO_DEFAULT_FROM_EMAIL is required when SMTP email delivery is configured."
    )

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

JWT_SIGNING_KEY = os.getenv("DJANGO_JWT_SIGNING_KEY", "").strip()
if not JWT_SIGNING_KEY:
    if not IS_LOCAL:
        raise ImproperlyConfigured("DJANGO_JWT_SIGNING_KEY is required outside local/test.")
    JWT_SIGNING_KEY = SECRET_KEY
elif not IS_LOCAL and len(JWT_SIGNING_KEY) < 50:
    raise ImproperlyConfigured("DJANGO_JWT_SIGNING_KEY must contain at least 50 characters.")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": JWT_SIGNING_KEY,
}

GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "").strip()
WEBAUTHN_RP_ID = os.getenv("WEBAUTHN_RP_ID", "localhost").strip()
WEBAUTHN_RP_NAME = os.getenv("WEBAUTHN_RP_NAME", "Dotick").strip()
default_webauthn_origin = "http://localhost:8081" if IS_LOCAL else ""
WEBAUTHN_ORIGIN = os.getenv("WEBAUTHN_ORIGIN", default_webauthn_origin).strip()
if not IS_LOCAL and not WEBAUTHN_ORIGIN.startswith("https://"):
    raise ImproperlyConfigured("Production WebAuthn origin must use HTTPS.")

FOUNDATION_ENABLED = IS_LOCAL and os.getenv("DOTICK_FOUNDATION_ENABLED", "0") == "1"
API_MAX_JSON_BODY_BYTES = 16 * 1024

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "DJANGO_CORS_ORIGINS",
        "http://127.0.0.1:8081,http://localhost:8081" if IS_LOCAL else "",
    ).split(",")
    if origin.strip()
]
if not IS_LOCAL and not CORS_ALLOWED_ORIGINS:
    raise ImproperlyConfigured("DJANGO_CORS_ORIGINS is required outside local/test.")
if not IS_LOCAL and any(not origin.startswith("https://") for origin in CORS_ALLOWED_ORIGINS):
    raise ImproperlyConfigured("Production CORS origins must use HTTPS.")
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOW_HEADERS = (*default_headers, "if-match")

SECURE_SSL_REDIRECT = not IS_LOCAL
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not IS_LOCAL
CSRF_COOKIE_SECURE = not IS_LOCAL
SECURE_HSTS_SECONDS = 0 if IS_LOCAL else 31_536_000
SECURE_HSTS_INCLUDE_SUBDOMAINS = not IS_LOCAL
SECURE_HSTS_PRELOAD = not IS_LOCAL
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "config.errors.api_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dotick.identity.authentication.SessionJWTAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"json": {"()": "config.observability.JsonFormatter"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "json"}},
    "root": {"handlers": ["console"], "level": os.getenv("LOG_LEVEL", "INFO")},
    "loggers": {
        "django": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "dotick.http": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
