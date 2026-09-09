"""Create private developer configuration without replacing existing settings."""

import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / ".env"
content = (
    path.read_text(encoding="utf-8")
    if path.exists()
    else (ROOT / ".env.example").read_text(encoding="utf-8")
)
for key in ("DJANGO_SECRET_KEY", "PGPASSWORD", "DOTICK_DEVELOPMENT_PASSWORD"):
    lines = content.splitlines()
    existing = next((line.split("=", 1)[1] for line in lines if line.startswith(key + "=")), None)
    if not existing:
        value = secrets.token_urlsafe(64 if key == "DJANGO_SECRET_KEY" else 32)
        content = (
            "\n".join(line for line in lines if not line.startswith(key + "="))
            + f"\n{key}={value}\n"
        )
path.write_text(content, encoding="utf-8")
print("Private configuration ready in .env. Existing values were preserved.")
print(
    "Developer email: developer@example.test. The password is DOTICK_DEVELOPMENT_PASSWORD in .env."
)
