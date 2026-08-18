# Dotick Deployment Baseline

> **Status:** Increment 0 baseline
> **Date:** 2026-08-17
> **Primary target:** reproducible local development and local-hosted Personal V1

# 1. Deployment units

Baseline Compose topology:

```text
reverse-proxy (production-like/local-hosted)
  +-- /api and /ws -> api (ASGI)
  +-- / -> client web build

api -> postgres
```

Development می‌تواند client dev server و Django dev server را جدا اجرا کند. PostgreSQL همچنان باید implementation واقعی integration tests باشد.

# 2. Environments

| Environment | Purpose | Data |
|---|---|---|
| local-dev | fast edit/test | disposable developer data |
| test/CI | deterministic verification | ephemeral database |
| local-hosted | Personal V1 runtime | persistent volume + backup |
| production-like | TLS/config/migration rehearsal | non-production data |

# 3. Configuration

- config از environment variables می‌آید.
- `.env.example` فقط نام و توضیح variableها را دارد، نه secret.
- required variable در startup validate می‌شود.
- حداقل: database URL/parts، Django secret، allowed hosts/origins، public API URL، environment name و log level.
- secure default برای محیط ناشناخته؛ debug به‌صورت پیش‌فرض خاموش.

# 4. Images and runtime

- imageها multi-stage و با version pin ساخته می‌شوند.
- container runtime با user غیرroot اجرا می‌شود.
- source development bind mount در local-hosted استفاده نمی‌شود.
- dependency install فقط از lockfile انجام می‌شود.
- image یک immutable artifact است؛ config در runtime تزریق می‌شود.

# 5. Database lifecycle

- PostgreSQL volume مسیر صریح و backupپذیر دارد.
- migration یک step کنترل‌شده پیش از rollout است، نه side effect هر replica startup.
- deployment قبل از migration پرریسک backup می‌گیرد.
- restore procedure باید حداقل یک بار پیش از Personal V1 release تمرین شود.
- downgrade با migration کور فرض نمی‌شود؛ rollback می‌تواند restore + previous image باشد.

# 6. Health and readiness

- `/health`: process زنده است؛ dependency detail فاش نمی‌کند.
- `/ready`: database و dependency ضروری قابل استفاده‌اند.
- external AI readiness برای core API شرط نیست.
- container healthcheck باید timeout و interval محدود داشته باشد.

# 7. TLS and networking

- local-hosted روی interface قابل دسترسی شبکه از reverse proxy TLS می‌گذرد.
- HTTP exception فقط برای loopback development است.
- database به public interface publish نمی‌شود.
- proxy header trust فقط برای proxy شناخته‌شده فعال می‌شود.

# 8. Logging and operations

- application log روی stdout/stderr ساخت‌یافته است.
- request id از proxy تا API propagate می‌شود.
- log rotation مسئول runtime/host است.
- backup failure، migration failure و readiness failure باید visible و actionable باشند.
- monitoring stack کامل تا نیاز عملی اضافه نمی‌شود، ولی health و structured logs از I0 حاضرند.

# 9. Clean-clone verification

Increment 0 زمانی از منظر deployment کامل است که روی clone تمیز بتوان:

1. dependencyها را از lockfile نصب کرد؛
2. PostgreSQL را بالا آورد؛
3. migration را اجرا کرد؛
4. API و client را build/start کرد؛
5. `/health` و `/ready` را بررسی کرد؛
6. Walking Skeleton را از client تا database اجرا کرد؛
7. test suite را با commandهای مستند اجرا کرد.

# 10. Deferred deployment choices

- cloud provider و managed services؛
- horizontal scaling؛
- Redis/channel layer؛
- worker scheduler؛
- mobile store release؛
- enterprise HA/SLA.
