# Agent Development Rules

**Objective:** Deliver the smallest complete, secure, user-accepted change. Optimize *time to accepted functionality*, not the volume of code, tests, or documentation.

**Process authority:** Read [docs/development/engineering-process.md](docs/development/engineering-process.md) for the continuous SDLC, release/slice workflow, risk-based verification and Definition of Done. The roadmap owns delivery sequencing, not product semantics. Follow the System Definition for accepted behavior until its replacement is explicitly approved. Historical increment procedures are not new mandatory gates.

## Before changing code
- Inspect only the relevant code, existing patterns, tests, and CI. Identify the observable outcome, acceptance criteria, non-goals, and risks. Ask only when a missing decision materially blocks safe work.
- Choose the lightest safe path by **risk, not change size**:
  - **A — Low:** copy, styling, isolated UI → implement directly; run relevant checks. No obligatory new spec, test, or document.
  - **B — Medium:** business logic, API, integration → brief plan if useful; focused behavior and integration tests; review the diff.
  - **C — High:** authentication, authorization, secrets, personal data, sync/conflict resolution, payments, destructive migrations → threat/risk review, independent positive and negative tests, rollback/recovery plan, and approval for consequential actions.

## Build and verify
- Deliver small, end-to-end, demonstrable **vertical slices**. Follow existing conventions; avoid speculative abstractions, unrelated refactoring, extra dependencies, and future features.
- Derive key expected results from requirements **independently of the generated implementation**. Test observable behavior at stable interfaces, real integration boundaries, and important user journeys. Avoid tautological assertions and excessive mocking; never weaken a test merely to make CI pass.
- Run relevant lint/typecheck/build/tests and, when applicable, the actual user flow. Investigate failures. Distinguish checks **run**, **failed**, and **not run**; never claim success without fresh evidence.
- Apply least privilege to agent tools and credentials. Never expose secrets or bypass security controls. Require explicit authorization for destructive or irreversible operations.

## Skills — invoke only when relevant
These skills are **optional**, not prerequisites. If installed, read the relevant `SKILL.md` and apply it only when its trigger matches; never run all skills as a pipeline. Do not silently install missing skills. Project rules and risk classification take precedence over skill defaults.
- `verification-before-completion`: before any completion, test-pass, or deployment claim; obtain fresh evidence.
- `code-review`: focused diff review against requirements and standards for B/C changes or when requested.
- `diagnosing-bugs`: reproduce a nontrivial failure and establish root cause before changing code.
- `webapp-testing`: verify changed browser/UI user journeys when relevant.
- `secure-software-engineering`: design or change security-sensitive behavior (level C).
- `product-shaping`: bound only large, ambiguous, or scope-creeping requests; skip for clear small changes.
Do not mandate TDD, ticketing, full security audits, or extra documents for every task. Prefer existing checks and files.

## Documentation and delivery
- Keep this file a short navigation and policy guide. Document only decisions, contracts, or constraints that are consequential, non-obvious, and difficult to recover from code or Git history. Prefer existing docs; avoid duplicate reports.
- Show or describe the working result against the acceptance criteria and seek Product Owner acceptance where required. Track escaped defects and rework alongside delivery speed. Improve recurring failure modes through tooling and automated guardrails, not more paperwork.
- Work on the specified existing Git branch only. **Never create a branch or PR (including draft), merge, force-push, rewrite shared history, delete branches, or perform destructive actions without explicit authorization.**
- Final report: what changed, acceptance/verification evidence, checks not run, remaining risks, and branch/commit status (if applicable).
