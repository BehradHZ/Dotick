# Dotick Engineering Process

> **Status:** Accepted — 2026-10-21. **Method:** Scenario-Driven Vertical Slice Development.
> **Goal:** The smallest complete, secure and user-accepted behavior with proportionate engineering—not maximum code, tests or paperwork.
> **Authority:** This document governs the development workflow. `AGENTS.md` governs short operational rules, the [roadmap](../planning/increment-roadmap.md) owns release grouping/order, and [Test Strategy](../quality/test-strategy.md) owns assurance details. Historical increment procedures are not current gates.

## 1. Unit of development

The implementation unit is the **smallest meaningful, independently demonstrable user behavior**: for example, “user signs in” or “user creates and later retrieves a Task”. It is not a database entity, a backend-only task, an arbitrary tiny issue, a fixed timebox or a complete epic. Finish relevant client, API, domain and persistence work (as applicable) in one slice. Group accepted slices into product-outcome increments/releases; provisional R1–R7 labels are organizational candidates, not approved scope.

Use continuous software engineering—requirements, domain analysis, architecture, implementation, verification, review and operations—at depth proportional to risk. No compulsory separate report for each SDLC stage, universal TDD mandate, or open-ended foundation-only implementation increment.

## 2. Engineering baseline

Before the rebuild, reconcile only consequential product/first-release scope, core domain invariants and lifecycles, architecture/modules, API/data contracts, identity and authorization, time/calendar, offline/sync compatibility, history/data ownership, security/recovery and quality decisions. Confirm actual stack decisions at the relevant architecture gate. Validate the baseline immediately with a working full user journey. Do not prebuild speculative enterprise features or generic frameworks. Historic v0.2.0 evidence is not proof of a Rust rebuild.

## 3. Mandatory scenario-driven cycle

**For every new product-behavior slice, the Agent proactively opens a dialogue with the Product Owner.** The owner approves observable behavior and important acceptance/test scenarios, **not** every low-level unit test. Keep explanations short, questions concrete and organized, and offer a recommended default with consequences. Never silently decide product ambiguity, repeatedly ask answered questions or require exhaustive imagined edge cases. Scale discussion depth with risk: a Low/A slice may require one concise exchange; a High/C slice may require several.

### Gate 1 — Behavior discovery (Agent + Product Owner)

- Propose **one** user-visible outcome, relevant dependencies, scope/non-goals and applicable existing decisions; challenge inconsistent or unnecessary prior complexity.
- Ask what happens from the user's perspective: entry, inputs/defaults, transitions, persistence, navigation, failure, cancellation, UI feedback and accessibility/responsive behavior where relevant.
- Group material unknowns with a suggested default and short trade-offs. Product Owner confirms the behavior and boundaries **before** coding.
- If a prerequisite (e.g. login for a private Task) matters, propose the smallest sensible order rather than silently implementing adjacent functionality.

### Gate 2 — Acceptance scenarios, edge cases and A/B/C (Agent + Product Owner)

- Convert approved behavior into **independently specified, observable scenarios**: main success; important invalid inputs, boundary conditions, error/network/retry and persistence paths; permission/privacy and interaction with existing features where material.
- Classify risk by the **highest possible impact**, not change size. Propose an explicit, concise verification plan: the relevant behavior to prove, test levels/integration boundaries, negative/security cases and what requires manual observation.
- Review the **scenario set and assurance level** with the Product Owner and obtain approval before implementation. The Agent independently authors the technical test details.
- Cover known important edge cases and plausible failures, **not every imaginable case**. Record minor out-of-scope/deferred cases and reopen this gate if new evidence changes behavior.

### Gate 3 — Technical analysis and just-enough design (Agent)

- Check domain invariants, states, module boundaries, API/schema/migrations, concurrency/idempotency, permissions, time, recoverability, known future compatibility and the agreed UI flow.
- Escalate only consequential product/architecture trade-offs or irreversible changes. Decide reversible implementation details independently. Avoid speculative abstractions and unrelated refactors.
- Resolve UI behavior before backend choices that would constrain it. Use an early sketch/prototype only if it materially reduces UX uncertainty; a polished screen is not required before logic.

### Gate 4 — Logic implementation and focused verification (Agent)

- Implement approved domain/application/API/persistence behavior; derive focused tests **from Gate 2, independently of generated code**.
- Verify affected invariants and integration boundaries; use real PostgreSQL for relevant PostgreSQL semantics. TDD is optional when useful, not compulsory.
- Backend success is an **internal checkpoint**, not a finished slice.

### Gate 5 — Complete base UI and integrate (Agent)

- Deliver the approved *base but precise* UI: relevant inputs/defaults, validation, loading, empty/error/success feedback, retry, accessibility/keyboard and responsive behavior.
- Connect the real client → API → domain → durable state flow as applicable; do not pass off a permanent mock or decorative UI as working functionality.
- Run the complete user journey and relevant integration/regressions. The preferred implementation sequence is logic then UI, but revise the interface or design earlier if that is necessary for correctness.

### Gate 6 — Agent verification and demonstration

- Review the diff, verify each approved acceptance criterion with fresh evidence, run risk-appropriate tests/static checks, real changed user flow and relevant regression. Diagnose failures; never weaken a test merely to turn CI green.
- Demonstrate a runnable result and report checks **passed, failed and not run**, plus residual risks and affected documentation/contracts. Preserve historical migrations/tests unless an approved, separately verified transition replaces them.
- The Agent cannot self-approve the Product Owner's acceptance.

### Gate 7 — Product Owner acceptance and real-use observation

- Product Owner tries the feature and responds **Accept**, **Changes Requested**, or **In Observation** for a period of firsthand use proportionate to risk. Do **not** require an arbitrary fixed waiting period for every slice.
- Agent helps with a concise walkthrough and suggests targeted things to observe. Fix discovered defects and verify regressions.
- Never close with an unresolved **critical/high-severity** defect. Minor nonblocking issues may be explicitly recorded and deferred with owner agreement. Do not automatically begin the next product behavior during unapproved observation.

### Gate 8 — Close and continue

- Close only after the Definition of Done and explicit Product Owner acceptance. Keep a compact scenario/verification/known-issues note near the relevant work; update living docs/roadmap only for actual consequential changes.
- Then suggest the next smallest complete behavior and return to Gate 1.

**State progression:** `Discovery → Scenarios Approved → Design Ready → Logic Implemented → UI Integrated → Agent Verified → In Observation → Accepted/Closed`; use `Blocked` or `Changes Requested` when appropriate. Return to an earlier gate when findings materially change requirements.

## 4. Risk-adaptive verification

| Risk | Typical slice/change | Required discussion/evidence |
| --- | --- | --- |
| A — Low | Isolated UI/copy/styling | Brief agreed outcome and obvious cases; applicable checks and direct inspection; no obligatory new test/spec/doc. |
| B — Medium | Task rules, API, transactions/integration | Agree significant positive/negative/boundary scenarios; focused behavior/integration tests, affected journey and diff review. |
| C — High | Sign-in/authentication, authorization, secrets, personal data, sync/conflict, destructive migration | Explicit failure/abuse/privacy/recovery cases; independent positive/negative tests, real relevant boundaries, safe rollout/rollback or recovery plan and approval for consequential actions. |

“User signs in” is C despite being a small user-visible slice. Reuse existing evidence and preserve important security/integrity coverage. Test UTC/timezone/DST, concurrency, retry/idempotency and access boundaries **where applicable**, not by blanket repetition. Distinguish automated checks from external-provider/device/recovery work not actually run. No arbitrary coverage percentage or exhaustive speculative test inventory is a completion goal.

## 5. Definition of Ready, Done and release

- **Ready to implement:** the outcome, key behavior, scope/non-goals, important edge cases, observable acceptance scenarios and A/B/C assurance approach were approved by the Product Owner; material design decisions are settled. Approving the test **plan** before implementation does not require coding every test first.
- **Agent Verified:** the relevant complete base UI → real API/domain → persisted behavior works; approved criteria and risk-relevant regression/security cases have fresh evidence; diff review occurred; passed/failed/not-run checks and residual risk are disclosed.
- **Accepted/Closed:** Agent Verified **plus explicit owner acceptance after suitable firsthand use**, no unresolved critical/high-severity problem, acknowledged minor deferrals, updated impacted contracts/docs and reported Git status. Neither a green compiler/CI nor backend-only success closes a behavior.
- **Release Done:** required slices accepted, plus proportionate integrated smoke, security, migration, deployment and recovery evidence. Closures do not impose a fixed calendar waiting period; respect actual dependencies and owner-directed sequencing.

## 6. Documentation ownership

| Artifact | Responsibility |
| --- | --- |
| Approved System Definition / Decision Register / SRS | Product behavior and consequential decisions/contracts until explicitly revised. |
| Domain Model, Architecture/ADRs, API schema and migrations | Invariants and costly-to-recover technical constraints. |
| [Roadmap](../planning/increment-roadmap.md) | Outcome grouping, slice sequence/dependencies and accepted progress. |
| [Test Strategy](../quality/test-strategy.md) | Test levels, CI policy and historical evidence, not owner acceptance. |
| `AGENTS.md` | Short stable operational rules and this-process pointer; **not** the separate copy/paste interaction instructions. |
| **This document** | The scenario-driven collaboration and stage gates. |

Keep the approved scenarios and verification evidence compactly in the relevant existing work item/document. Avoid a mandatory new document per gate or repetitive SRS/traceability/review reports. Historical I0/I1 documents remain historical evidence.

## 7. Research and continuous improvement

Recommendation research is a parallel, separate track with question, baseline, permission/data boundaries, reproducible evaluation and metrics; do not block ordinary todo use on experimental models. Refine guardrails in response to escaped defects, rework and observation feedback rather than adding universal paperwork.

## 8. Agent and Git safety

Follow `AGENTS.md`, use relevant skills selectively and minimum required tool privileges. Work only on the user-designated **existing** branch. Never create a branch/PR, merge, force-push, rewrite shared history, delete branches or undertake destructive actions without explicit authorization. Permission for this document change does not grant permission for future feature commits. Historical/provisional roadmap entries do not by themselves authorize implementing a feature.
