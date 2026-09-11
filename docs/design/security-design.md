# Dotick Security Baseline

> **Status:** Increment 1 backend baseline
> **Date:** 2026-09-08
> **Review cadence:** every security-relevant Increment

# 1. Scope and assets

دارایی‌های اصلی عبارت‌اند از account credential، session/token، private Item و organization data، history/audit data و secretهای provider. مرزهای اعتماد اصلی client/server، server/database و server/external provider هستند.

# 2. Baseline principles

- deny by default؛
- authorization server-side و مستقل از UI؛
- owner/group scope در ابتدای query؛
- کمینه‌سازی داده و privilege؛
- secret خارج از source control؛
- validation در مرز ورودی و invariant در domain/database؛
- log بدون credential/token/payload حساس؛
- external integration غیرقابل اعتماد و قابل قطع است.

# 3. Authentication baseline

I0 exception: the [developer-only foundation API](foundation-api.md) uses framework HTTP Basic authentication on loopback with explicitly provisioned test/developer accounts. Both environment and enablement guards prevent this workbench running as a product authentication surface. Credentials stay in client memory and are excluded from logs. The I1 [Authentication Design](authentication-design.md) implements the product identity backend; configured external-provider smoke remains a release gate.

- custom User model با UUID پیش از اولین migration.
- email/password، JWT، Google OAuth و Passkey در Increment 1.
- password فقط از API hashing استاندارد Django عبور می‌کند؛ Argon2 باید hasher ترجیحی باشد و fallback سازگار فقط برای migration/verification باقی بماند.
- plaintext password هرگز persist یا log نمی‌شود.
- reset/recovery code ده دقیقه عمر، single-use، HMAC-digested و پس از پنج تلاش ناموفق consumed است.
- access token پنج دقیقه و refresh token سی روز عمر دارد؛ refresh در هر استفاده rotate می‌شود و session-specific/all-session revocation در database enforce می‌شود.
- token در URL یا log قرار نمی‌گیرد.
- Google/Passkey identity به User داخلی link می‌شود و جای owner identity را نمی‌گیرد.
- Google identity با provider subject پایدار resolve می‌شود؛ تطابق email به‌تنهایی هرگز account موجود را auto-link نمی‌کند.
- Passkey challenge پنج دقیقه عمر و مصرف single-use دارد؛ enrollment و تغییر credential مستقل به session با authentication اخیر نیاز دارد.
- contact ثانویه تا تأیید code در هیچ فهرست active برگردانده نمی‌شود؛ کد فقط به adapter مقصد داده می‌شود و digest آن persist می‌شود.

# 4. Authorization baseline

- lookup الگوی `resource_id` و سپس permission check عمومی مجاز نیست؛ query باید از ابتدا scope کاربر داشته باشد.
- create باید ownership chain مقصد را validate کند.
- update/move باید source و destination هر دو در scope مجاز باشند.
- serializer/client-supplied `owner_user_id` منبع authority نیست.
- staff/admin access به‌طور پیش‌فرض business authorization را bypass نمی‌کند.
- Group role matrix در Increment 7 formalize می‌شود؛ تا آن زمان داده‌ی personal با owner scope محدود است.
- WebSocket آینده هنگام connection و هر subscription مجدداً scope را بررسی می‌کند.

# 5. Transport and browser security

- public و production-like endpointها فقط پشت HTTPS.
- HTTP فقط برای loopback local development مجاز است.
- reverse proxy باید redirect، HSTS در deployment مناسب و headerهای امنیتی را اعمال کند.
- `ALLOWED_HOSTS`, CORS و trusted origins allowlist هستند.
- cookie در صورت استفاده `Secure`, `HttpOnly` و `SameSite` مناسب دارد.
- اگر JWT در header استفاده شود، storage سمت client باید برای هر platform با threat model I1 تعیین شود؛ localStorage انتخاب پیش‌فرض بدون review نیست.

# 6. Input and data protection

- JSON body size، upload size و content type محدود می‌شود.
- ORM parameterization حفظ می‌شود؛ raw SQL نیازمند review و test است.
- خروجی RichDescription آینده باید در render boundary sanitize/encode شود.
- upload آینده با content validation، random storage name و malware policy وارد می‌شود.
- error عمومی اطلاعات stack، SQL، secret یا وجود resource خارج از scope را فاش نمی‌کند.
- backup شامل داده‌ی حساس است و همان access control و encryption محیط اصلی را نیاز دارد.

# 7. Logging and audit

مجاز:

- request/correlation id، route template، status، duration، actor id pseudonymous و event name.

ممنوع:

- password، authorization header، access/refresh token، OAuth code، passkey secret material، full user content و connection string.

AuditLog business در Increment 2 اضافه می‌شود و از operational log جدا است.

# 8. Dependency and delivery controls

- lockfileها commit می‌شوند.
- CI شامل dependency vulnerability scan و secret scan می‌شود.
- base image و runtime نسخه‌ی پشتیبانی‌شده و pin‌شده دارند.
- production container با user غیرroot و filesystem تا حد عملی read-only اجرا می‌شود.
- migration permission از runtime permission در production-like deployment قابل جداسازی است.

# 9. Required security tests

- cross-user read/update/delete/move denial؛
- forged owner/creator rejection؛
- inactive/expired/revoked credential rejection؛
- password hash و نبود plaintext در database/log؛
- CORS/host configuration inspection؛
- unauthenticated `/ready` بدون افشای dependency detail؛
- malformed/oversized input rejection؛
- WebSocket cross-scope tests در Increment 7؛
- cross-group matrix tests در Increment 7.

# 10. Deferred security decisions

- Google client، WebAuthn RP/origin و email/phone delivery configuration: deployment-specific I1 release gate.
- rate-limit thresholds: endpoint owner Increment.
- Group authorization model: I7.
- sync conflict trust model: I6.
- AI data retention/provider terms: I8/I9.
- Enterprise SSO/privacy/compliance: Enterprise scope.
