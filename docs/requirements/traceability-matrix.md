# Dotick Requirements Traceability Matrix

**Document type:** Requirements Traceability Matrix

**Version:** 2.1

**Baseline date:** 2026-08-26

**Implementation reconciliation:** 2026-09-06 — current SRS includes `SRS-SHARE-034`; total/family coverage is updated to 419 without changing requirement behavior.

**Status:** Reconciled Traceability Baseline for Formal SRS v2.9

**Scope:** Personal V1

> این سند مسیر `Canonical Behavior / Decision Rationale -> Formal Requirement -> Planned Increment` را ثبت می‌کند. این ماتریس منبع رفتار، Scope یا تصمیم جدید نیست. اگر behavior تغییر کند، ابتدا System Definition و در صورت نیاز Decision Register، سپس Formal SRS و در پایان این ماتریس update می‌شوند.

# 1. Purpose and authority

این baseline از `docs/requirements/srs.md` نسخه 2.9 و `docs/decision-register.md` فعلی regenerate و با Roadmap جاری reconcile شده است.

در تعارض درباره behavior یا Scope، ترتیب authority فعلی پروژه چنین است:

```text
System Definition
        ↓
Decision Register
        ↓
Formal SRS
        ↓
Domain Model / Design
        ↓
Roadmap / reconciled non-canonical references
        ↓
Traceability Matrix
```

بنابراین:

- `docs/requirements/system-definition.md` مرجع اول current behavior و Scope است.
- `docs/decision-register.md` مرجع دوم و مالک rationale، constraint و design handoff است.
- `docs/requirements/srs.md` رفتار canonical را به requirementهای atomic و testable تبدیل می‌کند.
- `docs/planning/increment-roadmap.md` فقط مالک ترتیب اجرا و Planned Increment است، نه behavior.
- این ماتریس فقط رابطه artifactها را ثبت می‌کند و نمی‌تواند requirement جدید بسازد، تعارض بالادستی را حل کند یا design/tuning detail را به Product Decision تبدیل کند.

# 2. Source key

| Code | Current repository document | Role |
|---|---|---|
| `SD` | `docs/requirements/system-definition.md` | primary current behavior and Scope authority |
| `DR` | `docs/decision-register.md` | decision rationale، constraints و design handoff |
| `SRS` | `docs/requirements/srs.md` | formal atomic requirements؛ baseline این ماتریس: v2.9 |
| `DM` | `docs/design/domain-model.md` | conceptual entities، relations و constraints؛ پایین‌تر از SRS در behavioral authority |
| `RM` | `docs/planning/increment-roadmap.md` | implementation order و owning Increment only |
| `TM` | `docs/requirements/traceability-matrix.md` | derived trace record؛ lowest authority in this chain |

# 3. Increment key

| Code | Increment |
|---|---|
| `I0` | Formal Specification + Engineering Baseline + Walking Skeleton |
| `I1` | Identity + Folder/List/Column + Basic Task MVP |
| `I2` | Complete Task/Event + Hierarchy + Description + Comments + Audit Foundation |
| `I3` | Routine + RoutineCompletion + TrackingState |
| `I4` | Recurrence + Routine Streak + Reminders + Time/Calendar Semantics |
| `I5` | Navigation + Views + Responsive UI + Themes |
| `I6` | Offline-first Sync + History + Undo |
| `I7` | Direct Sharing + Groups + Authorization + Assignment + Realtime |
| `I8` | AI-Assisted Item Creation — Voice Draft + Review |
| `I9` | Goal + AI Tags + Semantic Discovery + Goal Lifecycle |
| `I10` | Daily Rings + Dotick Day + Scoring + Norm + Statistics |
| `I11` | Personal V1 Production Readiness + Deployment |

# 4. Reconciliation summary

| Check | Reconciled result |
|---|---|
| Formal SRS baseline | v2.9، dated 2026-08-26 |
| Normative SRS requirements | **419** |
| Functional requirements (§3) | **370** |
| Interface/constraint requirements (§4) | **15** |
| Nonfunctional requirements (§5) | **34** |
| Requirement IDs without a family trace below | **0** |
| Current Decision Register records | **116** |
| Decision records with exact `Status: OPEN` | **0** |
| DRs directly named by normative SRS source preambles | **92** |
| Intentionally unspecified Current-Scope details | **26** non-normative design/tuning handoffs |

Verification روش هر requirement در همان atomic row از SRS v2.9 نگه‌داری می‌شود و در این سند دوباره copy نشده است؛ این کار از drift میان دو جدول جلوگیری می‌کند. Count و rangeهای زیر تمام 419 ID را پوشش می‌دهند.

# 5. Requirement-family traceability

`Canonical source(s)` همان source preamble بخش SRS یا normalization مستقیم آن است. اگر یک family میان چند Increment تقسیم شده، تفکیک ID در ستون `Planned ownership` آمده است. عددهای کوتاه مانند `001..005` به prefix همان row تعلق دارند.

| Requirement range | Count | SRS section | Canonical source(s) | Planned ownership |
|---|---:|---|---|---|
| `SRS-ORG-001..006` | 6 | §3.1 Organization، Inbox و navigation | SD §6.1؛ DR-001، DR-096؛ DM §15 | `I1`: 001..005؛ `I5`: 006 |
| `SRS-ITEM-001..010` | 10 | §3.2 Item، identity، ownership و source | SD §§6، 7.1؛ DR-012، DR-013، DR-111؛ DM §§2، 6 | `I1-I3`: 001؛ `I1`: 002..008؛ `I2-I3`: 009؛ `I2 + I4`: 010 |
| `SRS-TASK-001..032` | 32 | §3.3 Task | SD §6.2؛ DR-010، DR-011، DR-080، DR-081، DR-097؛ DM §4 | `I1`: 001؛ `I1 + I2`: 014؛ `I2`: all others |
| `SRS-EVENT-001..013` | 13 | §3.4 Event | SD §6.3؛ DR-015، DR-098، DR-115؛ DM §5 | `I2` |
| `SRS-HIER-001..017` | 17 | §3.5 Structural hierarchy and reference | SD §§6.4، 7.3، 7.4؛ DR-014، DR-015، DR-017، DR-099، DR-113، DR-114؛ DM §3 | `I2` |
| `SRS-DESC-001..005` | 5 | §3.6 RichDescription and ContentBlock | SD §6.5؛ DR-018، DR-019؛ DM §8 | `I2` |
| `SRS-COMMENT-001..006` | 6 | §3.7 Comment | SD §6.5؛ DR-100؛ DM §9 | `I2` |
| `SRS-ROUTINE-001..029` | 29 | §3.8 Routine | SD §6.6؛ DR-002..008، DR-083، DR-101؛ DM §§10..12 | `I3` |
| `SRS-RSTREAK-001..006` | 6 | §3.9 Routine streak | SD §6.6؛ DR-008، DR-095؛ DM §14 | `I4` |
| `SRS-REC-001..016` | 16 | §3.10 Recurrence | SD §6.7؛ DR-009، DR-082، DR-102؛ DM §13 | `I4` |
| `SRS-REM-001..006` | 6 | §3.11 Reminder | SD §6.8؛ DR-066، DR-103؛ DM §27 | `I4`؛ platform hardening in `I11` |
| `SRS-AUTH-001..015` | 15 | §3.12 Authentication and session | SD §§3.1، 6.13، 9.1؛ DR-048، DR-061، DR-128، DR-140 | `I1`؛ release hardening in `I11` |
| `SRS-VIEW-001..011` | 11 | §3.13 Views and presentation | SD §§1.4، 5.4.7، 6.1، 6.6، 10.6؛ DR-066، DR-133؛ RM I5 for presentation scope | `I5` |
| `SRS-SYNC-001..010` | 10 | §3.14 Offline use and sync | SD §§6.15، 8.5، 8.6؛ DR-047، DR-109، DR-122؛ DM §30 | `I6` |
| `SRS-AUDIT-001..009` | 9 | §3.15 Audit، History and Undo | SD §§6.12، 8.3، 8.4؛ DR-036، DR-072، DR-118؛ DM §25 | `I2`: 001..005 foundation؛ `I6`: 006..009 |
| `SRS-SHARE-001..034` | 34 | §3.16 Sharing، Group، Role and Assignment | SD §§3.1..3.4، 6.14، 7.1، 7.3، 7.4، 10.1؛ DR-054..057، DR-060..063، DR-093، DR-108، DR-109، DR-111، DR-113..115، DR-140؛ DM §29 | `I7` |
| `SRS-TAG-001..008` | 8 | §3.17 Tag | SD §6.9؛ DR-045، DR-104؛ DM §16 | `I2`: 001،003،005،008؛ `I2 + I9`: 002؛ `I9`: 004،006،007 |
| `SRS-GOAL-001..015` | 15 | §3.18 Goal and lifecycle | SD §6.9؛ DR-021، DR-023، DR-025، DR-026، DR-045، DR-089؛ DM §17 | `I9`: 001..009،015؛ `I9 + I10`: 010..012،014؛ `I10`: 013 |
| `SRS-GDISC-001..011` | 11 | §3.19 AI Goal discovery and GoalGenerationLog | SD §§5.4.3، 6.9، 8.9؛ DR-045، DR-046، DR-073، DR-085، DR-086، DR-104، DR-123؛ DM §18 | `I9` |
| `SRS-RING-001..021` | 21 | §3.20 Daily Ring selection، Daily Action and snapshot | SD §6.10؛ DR-024، DR-031، DR-043، DR-044، DR-049، DR-094؛ DM §§19، 20 | `I10` |
| `SRS-SCORE-001..014` | 14 | §3.21 Progress، completion، performance score and Norm | SD §6.10.6؛ DR-027..030، DR-070؛ DM §21 | `I10` |
| `SRS-DAY-001..014` | 14 | §3.22 Dotick Day and credited date | SD §§6.11، 8.1، 8.2؛ DR-033، DR-035، DR-115؛ DM §§22، 23 | `I10`: 001..012؛ `I0` baseline + `I2/I4/I10` refinement: 013..014 |
| `SRS-STAT-001..010` | 10 | §3.23 Statistics and historical correction | SD §§6.12، 7.2، 8.3؛ DR-036، DR-072؛ DM §24 | `I10` |
| `SRS-AIITEM-001..015` | 15 | §3.24 AI-assisted Item creation | SD §6.16؛ DR-037، DR-041، DR-042؛ AI-assisted creation domain model | `I8` |
| `SRS-AIEXEC-001..011` | 11 | §3.25 AI provider execution، BYOK and AI controls | SD §§5.4.3، 6.16، 9.2؛ DR-068، DR-126، DR-128 | `I8-I10`؛ release/security validation in `I11` |
| `SRS-NOTIF-001..009` | 9 | §3.26 Notification delivery and cross-device interaction | SD §§6.8، 8.7، 9.4؛ DR-103، DR-121، DR-128، DR-135 | `I4 + I7`؛ delivery hardening in `I11` |
| `SRS-CACHE-001..009` | 9 | §3.27 Attachment local cache | SD §§6.15، 11.2؛ DR-136 | `I6` |
| `SRS-DATA-001..008` | 8 | §3.28 Data export and Account deletion | SD §10.2؛ DR-131 | `I11` |
| `SRS-IF-001..005` | 5 | §4.1 API and client/server communication | SD §§4.1، 10.6؛ RM I0 engineering baseline | `I0 + I1`: 001..003،005؛ `I0 + I7`: 004 |
| `SRS-CON-001..004` | 4 | §4.2 Storage and platform constraints | SD §§4.1، 10.6؛ RM I0 engineering baseline | `I0`: 001..003؛ `I0 + I11` scope/deployment validation: 004 |
| `SRS-EXT-001..006` | 6 | §4.3 External service responsibility boundaries | SD §9؛ DR-048، DR-061، DR-065، DR-121، DR-128، DR-135 | `I1`: 001،002،006؛ `I7`: 003؛ `I4 + I11`: 004؛ `I0 + I11`: 005 |
| `SRS-NFR-SEC-001..011` | 11 | §5.1 Security | SD §10.1 and related Auth/Group behavior؛ DR-061، DR-126، DR-130 | continuous؛ primary owners `I1/I7/I8-I10/I11` by affected capability |
| `SRS-NFR-REL-001..008` | 8 | §5.2 Reliability and data protection | SRS §5.2؛ SD §§10.2..10.4 and related functional sources | cross-cutting؛ primary owners `I0/I3/I6/I8/I10/I11` by affected capability |
| `SRS-NFR-PERF-001..007` | 7 | §5.3 Performance | SRS §5.3؛ SD §10.5 and affected capability sources | cross-cutting؛ primary owners `I2/I5-I11` by affected capability |
| `SRS-NFR-UX-001..005` | 5 | §5.4 Usability and presentation | SRS §5.4 and affected View/Hierarchy/AI/Ring sources | primary owners `I2/I5/I8/I10` by affected capability |
| `SRS-NFR-MAINT-001..003` | 3 | §5.5 Maintainability and change isolation | SRS §5.5 and affected Source/View/PWA sources | cross-cutting؛ primary owners `I1/I5/I11` |

# 6. Decision Register traceability state

## 6.1 Current decision status

Decision Register فعلی **116** Decision Record دارد. هیچ record با exact status برابر `OPEN` وجود ندارد. عبارت‌هایی مانند `Open boundary` داخل بعضی DRها design/tuning handoff را نشان می‌دهند و نباید به‌عنوان Product/Domain decision باز یا requirement جدید تفسیر شوند.

Normative SRS source preambleها، با expand کردن rangeهایی مانند `DR-002 تا DR-008`، مستقیماً **92** DR را نام می‌برند. 24 DR زیر در preambleهای normative SRS به‌صورت مستقیم نام برده نشده‌اند:

`DR-020`, `DR-022`, `DR-050`, `DR-051`, `DR-052`, `DR-053`, `DR-058`, `DR-059`, `DR-064`, `DR-067`, `DR-069`, `DR-071`, `DR-074`, `DR-075`, `DR-076`, `DR-077`, `DR-078`, `DR-088`, `DR-091`, `DR-092`, `DR-141`, `DR-142`, `DR-143`, `DR-144`.

نبود direct citation در SRS به‌تنهایی traceability gap نیست. این گروه عمدتاً authority/document governance، product/design direction، scope/future boundary یا rationale کلی را ثبت می‌کند. اگر یکی از این DRها behavior الزام‌آور Current Scope ایجاد کند که در SRS v2.9 requirement متناظر ندارد، آن مورد باید ابتدا به‌عنوان SRS coverage defect ثبت و سپس با ID پایدار formalize شود؛ این ماتریس حق ایجاد requirement جایگزین را ندارد.

## 6.2 Replaced stale OPEN inventory

فهرست `OPEN-001..025` baseline قبلی حذف شده است، چون وضعیت فعلی را نادرست نشان می‌داد. موضوعات Product/Domain آن فهرست در Decision Register جاری بسته یا consolidate شده‌اند. موارد باقی‌مانده design، representation یا tuning هستند و با `UNSPEC-*`های SRS v2.9 trace می‌شوند.

# 7. Intentionally unspecified Current-Scope handoffs

این 26 row non-normative هستند. آن‌ها Product/Domain decision باز نیستند و acceptance behavior جدید ایجاد نمی‌کنند. owner فقط محل formalization جزئیات design/tuning را مشخص می‌کند؛ behavior باید با SD، DR و requirementهای §5 سازگار بماند.

| Detail ID | Intentionally unspecified detail | Owning artifact / gate |
|---|---|---|
| `UNSPEC-001` | RichDescription/ContentBlock schema، serialization، ordering و edit storage | Increment 2 Design |
| `UNSPEC-002` | structural child، dependency و reference schema/indexing | Increment 2 Data/API Design |
| `UNSPEC-003` | recurrence config serialization و occurrence persistence/identity | Increment 4 Recurrence/Data Design |
| `UNSPEC-004` | sync metadata، clock/device strategy، idempotency و conflict representation | Increment 6 Sync Design |
| `UNSPEC-005` | endpointها، payloadها و API versioning دقیق | per-Increment API Contract |
| `UNSPEC-006` | RingGroup/DailyAction physical representation و replan concurrency | Increment 10 Design |
| `UNSPEC-007` | Ring progress/final-score/early-bonus/late-recovery formula and coefficients | Increment 10 Scoring Specification |
| `UNSPEC-008` | Goal-selection algorithm، weights و learning parameters | Increment 10 Algorithm Specification |
| `UNSPEC-009` | difficulty/effort representation and estimation | Increment 10 Algorithm/AI Specification |
| `UNSPEC-010` | Adaptive Norm thresholds، windows و rate of change | Increment 10 Tuning Specification |
| `UNSPEC-011` | incremental Routine inactivity threshold and decay curve | Increment 3/10 Routine/Tuning Specification |
| `UNSPEC-012` | AI Goal warm-up duration | Increment 9 AI/Goal Specification |
| `UNSPEC-013` | numeric/model-specific Goal-similarity thresholds | Increment 9 AI/Goal Specification |
| `UNSPEC-014` | motivational/scolding timing، frequency، cooldown و copy | Increment 10 Gamification Specification |
| `UNSPEC-015` | Goal-level motivational-reminder frequency/rate limit | Increment 10 Gamification/Notification Specification |
| `UNSPEC-016` | contact verification-code format/expiry/retry/rate-limit، anti-abuse و normalization | Authentication/Security Design |
| `UNSPEC-017` | Attachment cache accounting، eviction، quota و platform storage | Offline/Storage Design |
| `UNSPEC-018` | encryption-at-rest algorithms، key management و storage-protection mechanism | Security Design |
| `UNSPEC-019` | backup frequency/retention/RPO/RTO and restore procedure | Operations/Security Design |
| `UNSPEC-020` | manual data-export format and Attachment packaging | Data/Export Design |
| `UNSPEC-021` | session hardening، account linking and credential recovery | Authentication Design |
| `UNSPEC-022` | service-managed AI routing/retry/timeout، BYOK storage and STT/provider implementation | AI/Security Design |
| `UNSPEC-023` | PWA service worker/install/offline-storage implementation and browser matrix | Client/PWA Design |
| `UNSPEC-024` | Notification transport/provider/device registration/retry | Notification Design |
| `UNSPEC-025` | prompt templates، model-specific parameters and detailed AI evaluation/tuning | AI Specification |
| `UNSPEC-026` | Time Semantics representation/storage and test-vector catalog | `docs/design/time-semantics-spec.md` / Recurrence & Time Design |

این inventory با SRS §7 و DR-144 هم‌مرز است: اگر Design یک سؤال واقعی Product/Domain کشف کند، آن سؤال باید به workflow تصمیم canonical برگردد و نباید با انتخاب implementation ضمنی بسته شود.

# 8. Increment 0 engineering-artifact trace

| Requirement(s) | Current engineering artifact | Current evidence boundary |
|---|---|---|
| `SRS-IF-001..004` | `docs/design/architecture.md`؛ `docs/design/adr/0001-modular-monolith-and-technology-stack.md` | client/server boundary، REST authority و WebSocket scope؛ implementation verification در Increment مالک باقی می‌ماند |
| `SRS-IF-005` | `docs/design/security-design.md`؛ `docs/operations/release-deployment.md` | TLS baseline و development exception boundary |
| `SRS-CON-001..003` | `docs/design/data-model.md`؛ `docs/design/adr/0002-explicit-item-composition-storage.md` | PostgreSQL و explicit-composition persistence baseline |
| `SRS-CON-004` | `docs/operations/release-deployment.md` | local development/deployment reality بدون ایجاد supported end-user self-hosting commitment |
| Increment 0 verification process | `docs/quality/test-strategy.md` | migration، integration، contract و Walking Skeleton gates |
| Increment risks | `docs/planning/risk-log.md` | architecture، isolation، reproducibility، recovery و cross-Increment risks |

## 8.1 Implemented foundation evidence — 2026-09-06

These are foundation-level checks, not completion claims for the full product requirement families.

| Requirement / gate | Implementation and verification |
|---|---|
| `SRS-IF-001..003`, I0 §7.5 | `apps/client/src/api.ts`, `apps/api/dotick/foundation/api.py`, `application.py`; `e2e/walking-skeleton.spec.ts` traverses the actual web/API/PostgreSQL stack |
| `SRS-IF-005`, `SRS-CON-004` | loopback-only development ports in `compose.yaml`; secure production settings check; production TLS deployment remains a later gate |
| `SRS-CON-001` | PostgreSQL identity/foundation migrations and API tests; clean container-database migration and readback |
| `SRS-CON-002..003` | explicit-composition ADR retained; disposable I0 records are isolated from the unimplemented Item schema |
| `SRS-NFR-SEC-001..003` foundation | Argon2 user model, owner-scoped queries, strict input and log allowlist; `test_foundation.py`, `test_security_baseline.py` |
| `SRS-DAY-013` | `docs/design/time-semantics-spec.md` |
| `SRS-DAY-014` foundation | `docs/design/time-vectors.json`, `apps/api/tests/test_time.py`, `apps/client/src/time-vectors.test.ts`; I4/I10 scenarios remain assigned, not marked executed |
| Increment 0 quality gates | `.github/workflows/ci.yml`, `scripts/check_traceability.py`, `docs/tracking/increment-0-foundation-review.md` |
| `SRS-AUTH-001..015`, I1-AC-01/02/09 backend | `apps/api/dotick/identity/`, migrations `0002..0007`, `docs/design/authentication-design.md`, `docs/design/openapi.json`, `apps/api/tests/test_identity_api.py`, `test_federated_identity_api.py`; configured external delivery/provider smoke remains open |
| `SRS-ORG-001..005`, `SRS-DAY-002`, I1-AC-03/08 backend | `apps/api/dotick/organization/`, `organization/0001_initial.py`, `apps/api/tests/test_organization_api.py`; atomic concurrent bootstrap, Inbox/default Column, optional Folder, ordering and recoverable container lifecycle |
| `SRS-ITEM-002..009`, `SRS-TASK-001/014/020`, I1-AC-04..08 | `apps/api/dotick/items/`, `dotick/tasks/`, `apps/client/src/`, API/component tests and `e2e/walking-skeleton.spec.ts`; explicit composition, owner/source identity, optimistic version, idempotency and Task Trash/restore |
| Increment 1 remaining acceptance | `docs/tracking/increment-1-readiness.md` retains configured provider/delivery, hosted CI and release evidence; local backend/client completion is not whole-increment release completion |

# 9. Update rules

در هر Increment، trace نهایی requirementهای در scope باید بتواند این مسیر را نشان دهد:

```text
System Definition section / Decision Register rationale
-> SRS Requirement ID
-> Planned Increment
-> Analysis / Acceptance Criteria
-> Design / API / Data / UI / ADR
-> Automated or Manual Verification
-> Implementation
-> Increment Review / Release
```

قواعد update:

- requirement جدید فقط پس از ورود با ID پایدار به Formal SRS وارد این ماتریس می‌شود.
- تغییر behavior ابتدا در System Definition، سپس در صورت نیاز Decision Register، بعد SRS و در پایان این ماتریس اعمال می‌شود.
- Roadmap می‌تواند ownership یا ترتیب اجرا را تغییر دهد، اما نمی‌تواند behavior requirement را تغییر دهد.
- `UNSPEC-*` فقط design/tuning handoff است؛ تبدیل آن به behavior جدید نیازمند workflow canonical است.
- Test ID، ADR، API operation، migration، module یا release فقط وقتی ثبت می‌شود که artifact واقعی وجود داشته باشد.
- requirement حذف‌شده از history محو نمی‌شود؛ superseding decision/SRS version باید قابل trace باشد.
- در پایان Increment، requirementهای owning Increment نباید بدون verification artifact و acceptance result باقی بمانند.
- هر بار SRS تغییر می‌کند، count کل IDها، uniqueness آن‌ها، family coverage و DR reference integrity باید دوباره بررسی شود.

# 10. Baseline status

این نسخه traceability را تا سطح `Canonical Source -> Formal Requirement Family/ID Range -> Planned Increment -> Verification Method in SRS` برای SRS v2.9 کامل می‌کند. Trace به Analysis، Design، Test Case، Code و Release با ایجاد artifactهای واقعی در Increment مالک تکمیل می‌شود.
