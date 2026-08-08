"""
Base Django settings for the Dotick project, shared by every environment.

Per ROADMAP.md §6 Stage 1: "settings split for local development" and
§3 (PostgreSQL as the chosen database). Environment-specific values
(secrets, hosts, debug flag) are read from environment variables here
so this file has no environment-specific hardcoding baked in — this
also anticipates Stage 4 (Docker), which requires env-var-based
configuration per §6.4.
"""

import os
from pathlib import Path

# BASE_DIR is the backend/ directory (two levels up from this file:
# dotick/settings/base.py -> dotick/ -> backend/).
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def _env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


# SECURITY WARNING: keep the secret key used in production secret!
# No hardcoded fallback for production use — local.py supplies a dev-only
# default so Stage 1 works out of the box without requiring env setup.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")

DEBUG = _env_bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

# CORS: the frontend (Expo web / phone browser) runs on a different
# origin than the backend (e.g. frontend on localhost:8081 or the
# laptop's LAN IP, backend on localhost:8000 or the LAN IP:8000), so
# every fetch() from the frontend is a cross-origin request. Without
# this, the browser silently blocks the response before it ever
# reaches the app's JS, which surfaces in the frontend as a generic
# "could not fetch" / TypeError: Failed to fetch — not an HTTP error,
# so it's invisible in Django's own logs.
#
# Origins are read from an env var so no LAN IP or port is hardcoded
# here (same env-var-driven approach as ALLOWED_HOSTS above, and
# anticipates Stage 4's containerized setup per ROADMAP.md §6.4).
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("DJANGO_CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dotick.urls"

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

WSGI_APPLICATION = "dotick.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# PostgreSQL per ROADMAP.md §3. Values come from environment variables;
# local.py / .env supplies real defaults for local development.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DOTICK_DB_NAME", "dotick"),
        "USER": os.environ.get("DOTICK_DB_USER", "dotick"),
        "PASSWORD": os.environ.get("DOTICK_DB_PASSWORD", "dotick"),
        "HOST": os.environ.get("DOTICK_DB_HOST", "localhost"),
        "PORT": os.environ.get("DOTICK_DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Django REST Framework — minimal config for Stage 1.
# Auth/permission scaffolding is intentionally left at DRF defaults;
# Stage 1 only needs a single unauthenticated health-check endpoint.
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}