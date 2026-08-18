# ADR-0001 — Modular monolith and technology stack

> **Status:** Accepted
> **Date:** 2026-08-17
> **Decision:** DR-053

# Context

Dotick به frontend/backend جدا، PostgreSQL، REST/JSON، مسیر mobile-first و local-hosted deployment نیاز دارد. پروژه در حال بازسازی document-first است و یک تیم کوچک باید بتواند بدون هزینه‌ی عملیاتی microserviceها Incrementهای متعدد domain را تحویل دهد.

# Decision

- backend: Python 3.14 + Django 5.2 LTS + Django REST Framework روی ASGI، مدیریت‌شده با `uv`؛
- frontend: Node.js 24 LTS + npm workspace + TypeScript + Expo SDK 57 + React Native + React Native for Web؛
- persistence: PostgreSQL؛
- architecture: modular monolith با domain/application/interface/infrastructure boundaries؛
- REST authoritative و WebSocket فقط برای live signalهای سبک؛
- dependencyهای optional مانند Channels، Redis، queue و AI SDK فقط در Increment نیازمند آن‌ها افزوده می‌شوند.

# Consequences

مزایا:

- auth، ORM، migration و admin tooling یکپارچه؛
- deployment ساده‌تر از distributed services؛
- reuse بالای client میان web و native؛
- boundaryهای قابل استخراج در آینده بدون پرداخت هزینه‌ی زودهنگام شبکه.

هزینه‌ها:

- discipline module boundary باید با review/test حفظ شود؛
- frontend و backend دو toolchain دارند؛
- realtime بعدی نیازمند ASGI/Channels یا adapter هم‌ارز خواهد بود.

# Rejected alternatives

- microservices: برای scope و اندازه‌ی تیم فعلی پیچیدگی عملیاتی نامتناسب دارد.
- server-rendered Django UI: با mobile-first/native direction هم‌راستا نیست.
- GraphQL as primary API: با REST requirement و نیاز فعلی سازگار نیست.
- انتخاب queue/Redis در Increment 0: use case مالک هنوز وجود ندارد.

# Primary references

- Django documentation: <https://docs.djangoproject.com/en/5.2/>
- Django REST Framework: <https://www.django-rest-framework.org/>
- Expo web development: <https://docs.expo.dev/workflow/web/>
- Expo monorepos: <https://docs.expo.dev/guides/monorepos/>
- Django Channels (deferred realtime adapter): <https://channels.readthedocs.io/en/stable/>
- Node.js release schedule: <https://nodejs.org/en/about/previous-releases>
- uv project and lockfile model: <https://docs.astral.sh/uv/guides/projects/>
