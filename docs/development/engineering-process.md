# Dotick Engineering Process

> **Status:** Accepted — 2026-10-20. Applies to the rebuild and subsequent work on the approved existing branch.
> **Purpose:** Deliver correct, secure, usable product capabilities with proportionate engineering effort—not maximum process artifacts.

## 1. Operating model

Dotick uses **iterative, incremental, outcome-driven development**. Each release boundary delivers a usable product outcome through one or more **end-to-end vertical slices** (client → API → application/domain → PostgreSQL, as applicable). Research work may proceed in parallel, but experimental recommendations must not block basic productivity workflows.

Software engineering remains continuous: requirements, domain analysis, architecture, implementation, verification, review, and operations are applied at the depth justified by the change. A step does not require a separate document merely because it exists in the SDLC.

## 2. Initial engineering baseline (before the first rebuild slice)

Review, reconcile, and keep only consequential foundations:

- Product vision, first usable release scope, accepted behavior, and exclusions.
- Domain concepts, invariants, lifecycle/state transitions, and time semantics.
- Architecture and module boundaries; Rust API, PostgreSQL and client responsibilities.
- Early compatibility decisions for identity/authorization, offline/sync, history/undo and data ownership; defer their full implementation until needed.
- Relevant security threats, data-loss/recovery strategy, API-contract conventions, and risk-based quality strategy.

This is **not** an independent, open-ended implementation increment. Validate the baseline immediately by delivering a real user journey. Do not prebuild generic frameworks, future enterprise structures or speculative integration layers.

## 3. Release and slice planning

A release is described by a **user-visible outcome**, not by its entity count, internal architecture layer, or fixed duration. Its scope may contain multiple slices; each slice must be demonstrable and integrate the necessary client/server/data path.

For each slice, record only:

1. Desired observable outcome and scope/non-goals.
2. Testable acceptance criteria, including relevant failure/permission behavior.
3. Material dependencies and risks; just-enough design when necessary.
4. Delivery and verification evidence, remaining risks, and Product Owner acceptance.

A code-only refactor or prerequisite is a task inside a release, not automatically a separate release. Product priorities and release order live in `docs/planning/increment-roadmap.md`; the roadmap does not override accepted product behavior.

## 4. Repeated engineering loop

**Define → Analyze/Design → Build → Verify → Review/Deliver.**

- **Define:** specify the user-facing outcome, accepted domain rules, and acceptance criteria before implementation.
- **Analyze/Design:** inspect the relevant code and constraints; decide the smallest complete solution and document only consequential new decisions.
- **Build:** deliver the whole slice using established conventions. Avoid speculative abstractions, premature dependencies and unrelated refactors.
- **Verify:** evaluate observed behavior against independently derived expectations. Run relevant static checks, tests, integration paths and actual user flows where applicable; investigate failures.
- **Review/Deliver:** inspect the diff, demonstrate acceptance, update only affected living documents, disclose unrun checks/risks and obtain acceptance when needed.

Return to earlier steps only when new evidence warrants it; this is not a mandatory multi-document waterfall or universal TDD ritual.

## 5. Risk-adaptive quality gates

| Risk | Typical change | Minimum proportionate evidence |
| --- | --- | --- |
| A — Low | Copy, styling, isolated presentation | Relevant checks plus inspection of the changed UI/behavior; no obligatory new spec/test/doc. |
| B — Medium | Domain logic, API, persistence integration | Focused behavior and integration tests, pertinent negative paths, diff review and affected user journey. |
| C — High | Authentication, authorization, personal data, sync/conflict resolution, destructive migrations | Explicit threat/failure review; independent positive and negative tests; real relevant integration boundaries; safe rollout/rollback or recovery plan; approval for consequential/irreversible actions. |

Risk is classified by possible impact, **not** lines changed. Existing tests may establish evidence; do not duplicate them for a coverage target. Never weaken tests to make CI pass. Use PostgreSQL when the behavior depends on PostgreSQL semantics. Regression tests are especially valuable for escaped defects, important invariants and previously broken journeys.

Maintain a lean CI: format/lint/typecheck/build, focused automated regression/integration/security checks, migration validation where relevant, and a real critical-path E2E smoke. Expand gates only when risk or observed failures justify them. Distinguish automated evidence from unrun external-provider, production-device and recovery checks.

## 6. Definition of Done

A slice is complete only when:

- Its accepted observable behavior works end-to-end, including meaningful errors and authorization boundaries.
- Relevant checks have actually run and passed; any unrun check or exception is named.
- Important data integrity, security and migration implications are addressed.
- The changed user journey is demonstrated or verified through a suitable stable interface.
- A focused review is complete; only impacted contracts/decisions/docs are updated.
- Residual risks and branch/commit state are disclosed; Product Owner acceptance is obtained when required.

A release adds integrated smoke/regression and deployment/recovery verification proportional to its exposure. A checklist or green compiler alone is not product acceptance.

## 7. Documentation ownership (no duplicates)

| Artifact | Owns |
| --- | --- |
| `docs/requirements/system-definition.md` (or its approved successor) | Current product behavior and scope. |
| `docs/decision-register.md` | Consequential decisions and rationale; supersede rather than duplicate. |
| `docs/design/domain-model.md` and `docs/design/architecture.md` | Domain invariants and meaningful structural/technical constraints. |
| API schema, migrations, relevant specialist designs | Executable contracts and implementation-specific irreversible decisions. |
| `docs/planning/increment-roadmap.md` | Outcomes, order, dependencies and current delivery status. |
| `docs/quality/test-strategy.md` | Detailed verification policy/gates, without repeating this process. |
| `AGENTS.md` | Short operational rules and pointers—not a second roadmap or process manual. |
| **This document** | Engineering workflow and cross-release delivery policy. |

Keep the SRS where it adds testable behavioral precision; do not mechanically copy every paragraph into the SRS, traceability matrix, tickets, diagrams and acceptance tests. Update living documents on actual changes. Historical reviews remain evidence, not current product authority.

## 8. Recommendation research track

Specify a separate research question, baseline, dataset/consent boundaries, evaluation protocol and metrics. Keep reproducible experiment results distinct from production acceptance. Introduce the earliest useful baseline with the first Goals/Recommendation slice; iteratively compare alternatives as real product feedback becomes available. The user-facing todo workflows must remain functional without the experimental model.

## 9. Agent execution and Git safety

Follow the approved `AGENTS.md` for tool use and delivery. Apply relevant skills selectively, not as a mandatory pipeline. Work only on the user-designated **existing** branch. Never create a branch/PR, merge, force-push, rewrite shared history, delete branches or make destructive changes without explicit authorization. Preserve unrelated existing work; never silently remove historical tests or migrations as part of process simplification.

## 10. Adoption and review

This document is the development-process source of truth. The root `AGENTS.md`, `docs/README.md`, roadmap and test strategy point here rather than duplicating its rules. Legacy increment details remain historical scope/reference material until product review approves revised release boundaries. Pilot the process on the first full Personal Planner user journey; track friction, escaped defects and rework, then refine based on evidence—not paperwork.
