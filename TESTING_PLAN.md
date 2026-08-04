# Dotick — Testing Plan

## 0. Purpose

This document is the testing companion to `ROADMAP.md`. For each stage of the
roadmap, it describes **what needs to be tested and why**, in plain language,
so each item can be translated directly into actual test code (unit,
integration, or manual) when that stage's implementation begins.

This plan is written for someone learning testing discipline for the first
time alongside the project — each section explains the *reasoning* behind why
a given case matters, not just a checklist of test names.

---

## 1. Testing Philosophy for This Project

- **Test-first where practical.** Per `ROADMAP.md` §2.3, tests are written
  before or alongside implementation, not bolted on afterward. For a first
  attempt at disciplined testing, "alongside" (write the test right after
  writing the smallest piece of logic it covers, before moving to the next
  piece) is an acceptable and realistic starting point — strict TDD
  (test-before-any-code) can be adopted once the rhythm feels natural.
- **Prioritize logic over plumbing.** Domain logic — status computation,
  postpone behavior, recurrence math — deserves thorough unit testing.
  Framework plumbing (Django's own ORM save/load behavior, for instance)
  does not need to be re-tested; trust the framework, test what's built on
  top of it.
- **Time-dependent logic is the highest-risk area in this project.** Because
  Task and Event status are computed from `now` (per `ROADMAP.md` §4.3,
  §4.5), nearly every bug risk in this system is a boundary-condition bug
  around timestamps. These get disproportionate testing attention below.
- **Two test levels are used throughout:**
  - **Unit tests** — a single function or model method, no database or
    network involved beyond what Django's test framework provides in-memory.
  - **Integration tests** — a full request/response cycle through an API
    endpoint, verifying the whole path (view → business logic → database →
    response) works together.

---

## 2. Stage 1 — Basic Foundation

**What's being tested:** not application logic yet — just that the
foundation is real and wired correctly. This stage's tests exist to catch
"it looks like it should work but the pieces aren't actually connected"
failures.

| Test | Type | Why it matters |
|---|---|---|
| Health-check endpoint returns a successful response | Integration | Confirms Django is running and routing works at all. |
| Health-check endpoint's response confirms a real database round-trip (not just a hardcoded response) | Integration | A hardcoded "OK" response would pass even if PostgreSQL were completely disconnected — this test must prove the database is actually reachable. |
| Frontend can successfully call the health-check endpoint and render the result | Manual (documented, not automated) | At this stage, an automated frontend test is disproportionate effort; a documented manual check (open on laptop, open on phone, confirm both show a live response) is sufficient and matches the stage's actual goal. |

**No domain logic tests belong in this stage** — there is no domain logic
yet by design.

---

## 3. Stage 2 — Core Task, Event, and Routine Management

This is the highest-risk stage in the whole roadmap: it introduces the CTI
schema, the full status model, postpone logic, and deadline history — all at
once, and all interdependent. Testing discipline here matters more than in
any other stage.

### 3.1 CTI Schema Tests

| Test | Type | Why it matters |
|---|---|---|
| Creating a Task also correctly creates its linked `base_events` row | Unit/Integration | Confirms the CTI parent/child relationship (`ROADMAP.md` §4.1) is wired correctly — a broken link here would silently corrupt every entity type. |
| Same test repeated for Event and Routine | Unit/Integration | Each child type needs its own confirmation; a bug specific to one child table wouldn't be caught by testing only Task. |
| Deleting a `base_events` row correctly deletes (or correctly blocks deletion of) its child row | Unit | Establishes and locks in the intended cascade behavior — this is exactly the kind of decision that's easy to get accidentally backwards. |
| Querying fields inherited from `base_events` (e.g., `title`) works correctly from a Task/Event/Routine instance | Unit | Confirms the inheritance actually exposes parent fields as expected, not just that the foreign key exists. |

### 3.2 Task Status Computation Tests

This is the single most important test group in the entire project, because
the status model (`ROADMAP.md` §4.3) is entirely time-driven and boundary
conditions are exactly where time-driven logic breaks.

| Test | Type | Why it matters |
|---|---|---|
| `now` before `due_date` → status is `TODO` | Unit | Baseline case. |
| `now` exactly equal to `due_date` → status is `TODO` (per the `<=` boundary in §4.3) | Unit | Off-by-one boundary errors are the most common bug class in date logic; the exact equality case must be pinned down explicitly, not left to whatever the code happens to do. |
| `now` just after `due_date`, before `deadline` → status is `OVERDUE` | Unit | Confirms the transition actually happens right after the boundary. |
| `now` exactly equal to `deadline` → status is `OVERDUE` (per the `<=` boundary) | Unit | Same boundary-precision reasoning as above, at the next transition point. |
| `now` just after `deadline`, before `deadline + grace_period` → status is `MISSED` | Unit | Confirms the second transition. |
| `now` exactly equal to `deadline + grace_period` → status is `MISSED` (inclusive boundary, per §4.3) | Unit | Same reasoning again — every boundary in this table needs its own explicit test, not just the "obviously inside" cases. |
| `now` just after `deadline + grace_period` → status is `AUTO_WONT_DO` | Unit | Confirms the final automatic transition. |
| `user_status = DONE` → status is `DONE` regardless of any timestamp values (test with timestamps that would otherwise produce every other status) | Unit | Confirms the explicit field always overrides the computed one, per §4.3 — this must hold even for a task whose deadline passed a year ago. |
| `user_status = WONT_DO` → status is `WONT_DO` regardless of timestamps | Unit | Same reasoning as above. |
| A task with `user_status = WONT_DO` can be reverted (field cleared) and correctly falls back to the appropriate time-computed status | Unit | Confirms the explicitly-designed reversibility (§4.3) actually works, not just that the initial write succeeds. |
| Status computation uses a mockable/injectable "current time" rather than calling the real clock directly inside the test | Unit (test infrastructure) | Without this, every test above is flaky by construction — tests must control `now` directly to test boundaries precisely, not rely on real wall-clock time during the test run. |

### 3.3 Event Status Computation Tests

| Test | Type | Why it matters |
|---|---|---|
| `now` before `start_time` → `UPCOMING` | Unit | Baseline. |
| `now` exactly at `start_time` → `ONGOING` | Unit | Boundary case, per §4.5. |
| `now` between `start_time` and `end_time` → `ONGOING` | Unit | Baseline. |
| `now` exactly at `end_time` → `ONGOING` (inclusive, per the `<=` in §4.5) | Unit | Boundary case. |
| `now` after `end_time` → `PAST` | Unit | Baseline. |

### 3.4 Routine Instance Status Tests

| Test | Type | Why it matters |
|---|---|---|
| Manually created routine instance defaults to `TODO` | Unit | Baseline for Stage 2's manual-entry routine support (full recurrence is Stage 3). |
| `user_status = DONE` / `WONT_DO` behave the same as Task's explicit-field override | Unit | Confirms the shared pattern between Task and Routine (§4.6) is actually implemented consistently, not duplicated with subtle differences. |
| `WONT_DO` reversibility works the same as for Task | Unit | Same reasoning as §3.2. |

### 3.5 Postpone Logic Tests

| Test | Type | Why it matters |
|---|---|---|
| Postponing a `TODO` or `OVERDUE` task sets `due_date` to today and leaves `deadline` unchanged | Unit | Confirms the first branch of §4.7's two-behavior split. |
| Postponing a `MISSED` task sets `due_date` to today **and** advances `deadline` | Unit | Confirms the second branch — this is the case most likely to be implemented incorrectly if the two branches share code carelessly. |
| Postponing a `MISSED` task produces a `deadline` that is genuinely in the future (not just "different") | Unit | Guards against an off-by-something bug where the deadline shifts but not enough to actually resolve the missed state. |
| "Postpone All" applied to a mixed set of `OVERDUE` and `MISSED` tasks applies the correct branch to each individually | Integration | This is the case most likely to break if "Postpone All" is implemented as a naive single rule applied to everything, instead of correctly dispatching per-task. |
| "Postpone All" does not affect tasks that are `TODO`, `DONE`, or `WONT_DO` | Integration | Confirms the bulk action's scope is correctly limited — an overly broad implementation could accidentally un-complete finished tasks. |
| Postpone action on a task correctly triggers a `TaskDeadlineHistory` write when `deadline` changes | Integration | Connects §4.7 and §4.8 — this is exactly the kind of cross-feature interaction that's easy to forget when each piece is built and tested in isolation. |
| Postpone action that only changes `due_date` (not `deadline`) does **not** produce a `TaskDeadlineHistory` row | Unit/Integration | Confirms the history table stays scoped to actual deadline changes, not every postpone action indiscriminately — assuming the open item in `ROADMAP.md` §9.2 is resolved as "deadline-only" scope; revisit this test if that scope decision changes. |

### 3.6 Deadline History Tests

| Test | Type | Why it matters |
|---|---|---|
| A direct manual edit to `deadline` (outside the Postpone flow) produces a history row with `reason = MANUAL_EDIT` | Integration | Confirms the history table captures *all* deadline changes, not just ones that go through Postpone — per §4.8. |
| A `POSTPONE_SINGLE` action produces a history row with the correct `reason` value | Integration | Confirms the reason enum is set correctly per code path, not defaulted or guessed. |
| A `POSTPONE_ALL` action produces history rows with `reason = POSTPONE_ALL` for every affected task | Integration | Same reasoning, for the bulk path specifically. |
| History rows are ordered correctly and `old_deadline`/`new_deadline` values are accurate across a sequence of multiple changes to the same task | Integration | The real value of this table is reconstructing a sequence of changes — a single-write test isn't enough to confirm the sequence stays coherent. |

### 3.7 CRUD Endpoint Tests

| Test | Type | Why it matters |
|---|---|---|
| Create/read/update/delete for Task, Event, and Routine each work via the API | Integration | Baseline confirmation that the endpoints exist and function, separate from the domain-logic tests above. |
| Invalid input (e.g., `due_date` after `deadline`) is rejected with a clear error, not silently accepted | Integration | This constraint is implied by the domain model (`due_date <= deadline`) but needs an explicit test to confirm it's actually enforced, not just assumed. |

---

## 4. Stage 3 — Recurrence Engine

Recurrence is the second-highest-risk area in the roadmap, because calendar
math (especially across two calendar systems) is a well-known source of
subtle, hard-to-notice bugs.

| Test | Type | Why it matters |
|---|---|---|
| Daily recurrence generates one instance per day over a test range | Unit | Baseline. |
| Every-N-days recurrence generates instances at the correct interval | Unit | Baseline, but confirm with an N that doesn't divide evenly into common periods (e.g., N=5) to catch off-by-one interval bugs. |
| Specific-weekdays recurrence (e.g., Tue/Wed/Fri) generates instances only on the correct days over a multi-week range | Unit | Confirms weekday selection logic, tested across at least two full weeks to catch week-boundary bugs. |
| Day-of-month recurrence (Gregorian) generates the correct date in a normal month | Unit | Baseline. |
| Day-of-month recurrence (Gregorian), target day 31, correctly clamps in a 30-day month and returns to the 31st in the next 31-day month | Unit | This is the exact edge case called out in `ROADMAP.md` §4.9 — it must be tested explicitly, not assumed to work because the normal case works. |
| Day-of-month recurrence (Gregorian), target day 31, correctly clamps to 28 or 29 in February depending on leap year | Unit | Leap year handling is a classic source of date bugs; test both a leap and non-leap year explicitly. |
| Day-of-month recurrence (Jalali), target day 31, correctly clamps in Esfand | Unit | Same reasoning as above, for the Jalali calendar specifically — do not assume Gregorian-calendar test coverage implies Jalali correctness, since the two calendars have different leap-year rules. |
| A recurrence rule originally defined in one calendar system continues to produce dates from that calendar's rule, even if the equivalent converted date in the other calendar would differ | Unit | This directly tests the "preserve the original calendar as source of truth" rule in §4.9 — without this test, a future refactor could silently start recomputing from a converted date instead of the stored original. |
| Generated recurring instances correctly integrate with Stage 2's status logic (a generated instance starts as `TODO` and follows the same computed-status rules) | Integration | Confirms Stage 3 doesn't accidentally bypass or duplicate the status logic already tested in Stage 2 — recurrence should generate ordinary instances, not a parallel status system. |
| Migration of Stage 2 manually-created routine instances into the Stage 3 recurrence-backed model preserves existing completion history | Integration | This is a one-time but high-stakes operation — a bug here silently destroys real usage data from Stage 2, which by the roadmap's own progression rule (§2.5) will exist by the time Stage 3 begins. |

---

## 5. Stage 4 — Containerization (Docker)

Containerization tests are about **operational correctness**, not new domain
logic — the goal is confirming nothing was lost in translation, not testing
new business rules.

| Test | Type | Why it matters |
|---|---|---|
| `docker compose up` brings up backend and database successfully from a clean state | Manual/Integration | Baseline — the core promise of this stage. |
| All Stage 2/3 integration tests pass when run against the containerized stack, not just the native local setup | Integration | This is the real regression check for Stage 4 — it confirms containerizing didn't silently change behavior (e.g., timezone handling differences between the native environment and the container). |
| Environment-variable configuration correctly overrides defaults (e.g., database credentials) without requiring code changes | Integration | Confirms the configuration approach described in `ROADMAP.md` §6 Stage 4 actually decouples config from code, rather than just moving hardcoded values from one file to another. |
| Data persists correctly across a container restart (verifies volume configuration) | Manual/Integration | A very common containerization mistake is losing database data on restart because a volume wasn't configured — this must be explicitly verified, not assumed. |

---

## 6. Stage 5 — Organizational Hierarchy

Detailed tests for this stage depend on the structural decisions the
developer has made separately and recorded in `ROADMAP.md` §6 Stage 5 once
that section is filled in. The categories below are placeholders describing
the *kinds* of tests this stage will need, to be made concrete once the
structure is finalized:

| Test category | Why it will matter |
|---|---|
| Organizational entity CRUD | Same baseline reasoning as Stage 2's CRUD tests. |
| Association between organizational entities and Task/Event/Routine | Confirms items correctly belong to the folders/lists/tags they're assigned to, and that reassignment works correctly. |
| Per-list `grace_period` migration from Stage 2's provisional per-task default | This is a data migration with the same stakes as the Stage 3 routine-instance migration — existing tasks must end up with a correct, sensible grace period after the migration, not a lost or default-reset value. |
| Per-list `grace_period` correctly affects the `MISSED` → `AUTO_WONT_DO` computation from §3.2 | Integration test connecting Stage 5 back to Stage 2's core logic — confirms the two stages' logic actually composes correctly rather than just coexisting. |

This section should be expanded with concrete test cases once Stage 5's
detailed design is recorded in `ROADMAP.md`.

---

## 7. Cross-Cutting Testing Notes

- **Timezone handling** is not called out as a separate stage but touches
  every time-based test above. Decide early (Stage 2) whether all timestamps
  are stored and compared in UTC with conversion only at display time, and
  write at least one explicit test confirming a task's status computes
  correctly for a user in a timezone where "today" locally is a different
  date than "today" in UTC. Getting this wrong is one of the most common
  sources of date-logic bugs and is easy to miss if all early testing happens
  in a single timezone.
- **Test data time control:** as noted in §3.2, tests that depend on "now"
  need a way to control what "now" means during the test run. Establish this
  pattern once, early in Stage 2, and reuse it for every subsequent
  time-dependent test in Stages 3 onward, rather than reinventing it per
  stage.
