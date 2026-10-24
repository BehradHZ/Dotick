# Dotick — Documentation-First Rebuild Plan

**Status:** Planning-only reset; no new product behavior, technology choice, or implementation approved.
**Date:** 2026-10-24. **Target branch:** `main`.

## Goal and starting point
Recreate all active Dotick documents **from the Product Owner-approved narrative** rather than editing old specifications into compliance. The edited “یک روز با Dotick” is not yet a finalized repository baseline; it must first receive explicit approval. Legacy documents, architecture, code and tests are historical references, not automatically binding decisions or proof of a new implementation.

The predecessor `main` commit was `8cff0c021d3853b8cd787da3e6acf85adb89d817`. Preserve its history without force-push or history rewrite. See [ARCHIVE_INDEX.md](docs/archive/legacy-2026-10-24/ARCHIVE_INDEX.md) for retained historical reference files, exact source commits, and archival tags.

## Sequence: create progressively, not as one bulk document dump

### 0. Approve the Product Scenario — NEXT ACTION
- Review the exact latest narrative with the Product Owner, including Current / Future / Out-of-Scope.
- Resolve meaningful differences without silently restoring old decisions: Task Dependency satisfaction; Parent Done cascade preference; Column deletion destinations; recurrence-edit preference; Google identity assertion versus Dotick's own account/session.
- Save the **explicitly approved** narrative as `docs/product/product-scenario.md`, recording status/date.
- No feature coding before the appropriate behavior/acceptance gates.

### 1. Product foundation
Create:
- `docs/product/product-vision.md`: problem, users, promise, principles.
- `docs/product/product-scenario.md`: approved original narrative.
- `docs/product/product-scope.md`: Current/V1, Future, Out-of-Scope.
- `docs/product/user-personas.md`: relevant actors and goals, without invented user research.
- `docs/product/capability-map.md`: map **every** narrative capability and gap.
- `docs/product/glossary.md`: canonical meaning of domain terms.

Exit: coherent product identity and all story sections covered.

### 2. Requirements baseline
Create:
- `docs/requirements/behavior-catalog.md`: independent observable behaviors; IDs, outcome, dependencies, scope and risk.
- `docs/requirements/system-definition.md`: canonical, technology-independent behavior and invariants.
- `docs/requirements/srs.md`: specific testable requirements derived from that behavior.
- `docs/requirements/non-functional-requirements.md`: security, privacy, integrity, offline, reliability, performance and UX expectations.
- `docs/decisions/decision-register.md`: consequential decisions, alternatives, rationale and supersession.
- `docs/README.md`: ownership, status, and authority of active docs.

Exit: no material contradictions; Product Owner approves consequential product choices. The approved story establishes intent; System Definition is the canonical detailed current behavior; SRS formalizes its verification.

### 3. Domain and UX design together
Create, as needed:
- `docs/design/domain-model.md`, `state-machines.md`, `time-semantics.md`, `authorization-model.md`.
- `docs/ux/information-architecture.md`, `user-flows.md`, `interaction-specification.md`, `design-system.md`.

Resolve user-visible options and consequences **before** choosing a backend representation that locks those decisions. Treat source truth, finalization, actor/creator/ownership, scheduling, sharing, permissions and offline acceptance explicitly.

### 4. Just-enough architecture and technical contracts
As owning slices require, create `docs/design/system-architecture.md`, `data-design.md`, `api-contract.md`, `offline-sync.md`, `ai-system.md`, `notification-system.md`; record costly architectural choices under `docs/decisions/adr/`.

Settle foundational high-impact contracts early: identity, authorization, ownership, time/calendar, versioning, history, sync compatibility, security and recovery. Do not prebuild speculative Future features or silently reuse the historical technology stack.

### 5. Engineering, quality and operations
Create `docs/development/engineering-process.md`, `coding-standards.md`, `development-setup.md`, `docs/quality/test-strategy.md`, and concise `docs/quality/acceptance-scenarios/` where valuable. Prepare `docs/operations/deployment.md`, `security.md`, `backup-recovery.md` as needed. Adopt a new root `AGENTS.md` when the process is approved.

**Mandatory working method: Scenario-Driven Vertical Slice Development.** Each new user-visible outcome requires:
1. Agent-led Behavior Discovery with Product Owner: trigger, input/default, success/state, invalid input, error/retry/cancel, persistence/integration, and UI feedback.
2. Product Owner approval of intended behavior/scope.
3. Independently specified observable acceptance scenarios, negative/security/boundary cases and risk A/B/C verification plan; Product Owner approval of important scenarios and test approach.
4. Just-enough design → domain/application → API/persistence → focused tests → complete base UI → real integration.
5. Fresh changed-flow/regression/security verification, diff review and honest passed/failed/not-run report.
6. Product Owner outcome: **Accept / Changes Requested / In Observation**. Only explicit acceptance closes the slice; do not implement the next behavior automatically.

No mandatory new document for every gate, no backend-only completed slices, no mocks presented as production behavior, no fixed observation period.

### 6. Delivery plan and first slice
Create:
- `docs/planning/product-roadmap.md` — behavior ordering and dependency.
- `docs/planning/release-plan.md` — coherent grouping of accepted slices.
- `docs/planning/delivery-tracker.md` — status, verification evidence, blockers and owner acceptance.

Propose the smallest first runnable user flow only after approved scope and necessary early contracts. Roadmap orders delivery; it does not invent feature behavior or authorize coding by itself.

## Intended directory map
```text
README.md
REBUILD_PLAN.md
AGENTS.md                      (new, after process approval)
docs/
  README.md
  product/                     vision, scenario, scope, personas, capability map, glossary
  requirements/                behavior catalog, system definition, SRS, NFRs
  decisions/                   decision register, adr/
  design/                      domain, state, time, authorization, architecture,
                               data, API, offline-sync, AI, notification
  ux/                          IA, user flows, interaction spec, design system
  development/                 engineering process, coding standards, setup
  quality/                     test strategy, acceptance scenarios/
  planning/                    roadmap, release plan, delivery tracker
  operations/                  deployment, security, backup/recovery
  archive/legacy-2026-10-24/   frozen reference material
```

Only create real content at the stage that owns it. Do not fabricate unapproved details to fill a template.

## Working safeguards
- Archive is read-only history; previous decisions do not become active unless reconsidered and accepted.
- Work on `main` as explicitly designated for this reset. Later work on any branch requires explicit designation.
- Never create branches/PRs, merge, force-push, rewrite history, or perform destructive changes without new authorization.
- Do not claim runnable functionality, successful tests or deployment from a docs-only reset.

**Immediate next step:** approve the exact Product Scenario, then author `product-scenario.md` and `capability-map.md`.
