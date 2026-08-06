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
