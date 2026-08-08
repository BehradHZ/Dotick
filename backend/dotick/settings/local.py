"""
Local development settings.

Used when running the backend directly on the developer's laptop
(ROADMAP.md §1.2: "the developer's own laptop acting as the server").
Loads variables from a .env file if present (see .env.example), then
layers dev-friendly defaults on top of base.py for anything not set.

Run with: DJANGO_SETTINGS_MODULE=dotick.settings.local
(this is also manage.py's default — see manage.py).
"""

import os

from dotenv import load_dotenv

load_dotenv()

# Import after load_dotenv() so base.py's os.environ.get() calls see
# values from .env.
from .base import *  # noqa: E402,F401,F403

# Dev-only fallback secret key so `python manage.py runserver` works
# immediately after cloning, with no .env required. Never used if
# DJANGO_SECRET_KEY is set (including in any non-local settings module).
if not SECRET_KEY:
    SECRET_KEY = "django-insecure-dev-only-key-do-not-use-in-production"

DEBUG = True

# Reachable from the phone and laptop browser on the same local network
# (ROADMAP.md §1.2), plus localhost for the laptop itself.
_default_hosts = ["localhost", "127.0.0.1"]
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS + _default_hosts))

# If a wildcard LAN host is provided via env (e.g. DJANGO_ALLOWED_HOSTS
# includes the laptop's LAN IP), it's already picked up by base.py above.

# Dev-friendly CORS defaults so `expo start --web` works out of the box
# against a freshly cloned repo, with no .env required (mirrors the
# SECRET_KEY fallback above). Covers Expo's default web ports across
# versions/tools (8081, 19006) on both localhost and 127.0.0.1.
# Real deployments must set DJANGO_CORS_ALLOWED_ORIGINS explicitly —
# these defaults are dev-only and never used if that env var is set.
_default_cors_origins = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
    "http://localhost:19006",
    "http://127.0.0.1:19006",
]
CORS_ALLOWED_ORIGINS = list(dict.fromkeys(CORS_ALLOWED_ORIGINS + _default_cors_origins))

# The phone on the LAN uses the laptop's LAN IP, not localhost, for
# both the frontend origin and the backend host — that IP can't be
# guessed here, so it must come from DJANGO_CORS_ALLOWED_ORIGINS /
# DJANGO_ALLOWED_HOSTS in .env when testing from a phone. See
# ../../frontend/.env.example and ../.env.example.