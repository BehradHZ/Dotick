# Dotick — Foundational Decisions

This document precedes any diagramming or code. It exists to answer three questions, each with a defensible reason:

1. Which software process model governs development, and why not the alternatives?
2. Which diagrams are worth producing at this stage, and in what order?
3. Which technology stack was chosen, and why?

This is itself an SE deliverable in the spirit of the roadmap's own rule: *"each stage should include a short written explanation of the key decisions made and why alternatives were not chosen."*

---

## 1. Process Model

### 1.1 Decision: Incremental Development Model

Dotick follows an **incremental process model** (Pressman, Ch. 4): the system is built as a series of stages, each producing a usable increment, each used in practice before the next stage begins. This is already expressed in `ROADMAP_formal.md` — this section makes the reasoning explicit and defends it against the standard alternatives.

**Precondition check.** Pressman's incremental model assumes *basic requirements are reasonably well understood* before staging begins, even if implementation detail is not. That precondition holds here: the two core problem statements (date/deadline separation; non-corrupting routine tracking) are stable and unlikely to change. What remains open — the rollover/routine data model, the template system architecture — are **implementation-design questions**, not requirements gaps. The incremental model doesn't require those to be resolved up front; it requires the *problem* to be understood, which it is.

### 1.2 Why not Scrum or XP

Scrum and XP are built around a **fixed-cadence iteration** (Scrum: 1–4 week sprints; XP: typically 1–2 weeks) and a **whole-team structure** that includes a distinct customer role providing and prioritizing work.

Neither assumption holds for this project:

- **No fixed cadence is meaningful.** Development time is solo and variable week to week, with no deadline. A sprint boundary would be arbitrary — there's no team to synchronize with, no velocity to track against a shared commitment, and no cost to letting a stage run long if real use hasn't yet produced a lesson worth acting on. Imposing sprint boundaries here would be process theater, not process value.
- **The customer/developer split doesn't exist.** XP in particular assumes a negotiation loop between "the team" and "the customer" — someone who writes stories, sets priorities, and is available for continuous feedback. Here, the developer and the sole intended user are the same person. There's no negotiation to structure, because there's no second party. The mechanism XP is built around (bridging developer and customer perspectives) is solving a problem this project doesn't have.

Scrum/XP practices aren't rejected wholesale — daily "what did I learn," short-lived plans, and continuous refactoring are compatible with incremental staging and can be borrowed informally. What's rejected is the *scaffolding* (timeboxed sprints, backlog grooming ceremonies, a customer role) that exists to coordinate people who aren't present in a one-person project.

### 1.3 Why not Unified Process (or RUP)

UP's four-phase structure (Inception → Elaboration → Construction → Transition) is architecture-centric and produces a defined set of formal artifacts per phase — Vision documents, an SRS, a Software Architecture Document, a Software Development Plan, a Business Case, and so on, each revised at every phase boundary.

This is rejected on **overhead grounds**: UP's artifact set is sized for a project with multiple stakeholders who need a shared, durable record to coordinate against. For a solo portfolio project, producing and maintaining a Vision document, SDP, and SAD in parallel with the software itself would consume time better spent building and using the actual increments — which is the roadmap's stated priority ("something that can actually be used, not just planned"). UP's discipline is valuable in spirit (this document exists because of that same instinct — document key decisions before they're lost), but its full artifact machinery is disproportionate to the team size of one.

### 1.4 Summary comparison

| Model | Core assumption that fails here | Verdict |
|---|---|---|
| Waterfall / V-Model | Requirements fully known and stable before design begins; no room for after-the-fact change | Rejected — contradicts the explicit goal of organic, module-level design emergence |
| Scrum | Fixed sprint cadence with a team to synchronize | Rejected — no team, no meaningful cadence |
| XP | Customer role distinct from developer, providing continuous story input | Rejected — developer *is* the customer |
| Unified Process / RUP | Justifies formal artifact overhead (SAD, SDP, Business Case) via multi-stakeholder coordination need | Rejected — overhead disproportionate to a one-person team |
| **Incremental (chosen)** | Requires basic requirements to be understood, not implementation detail to be finalized | **Fits** — problem statement is stable; only design mechanics remain open |

---

## 2. Diagram Plan

Diagrams are tools for resolving specific open questions or communicating a specific structure — not a checklist to complete. The two architectural prerequisites (rollover/routine interaction; template system architecture) will be settled in a dedicated design session *before* diagramming begins, so that diagrams document a decision rather than accidentally making one by default of notation.

### 2.1 Diagrams planned, in order

| Order | Diagram | Purpose | When |
|---|---|---|---|
| 1 | **Use-case diagram** | Scope Stage 2 (task CRUD) and confirm actor boundaries before any class modeling starts | After Stage 2 requirements are finalized |
| 2 | **State diagram** (per task/routine instance) | Once the rollover/routine decision is made, this is the artifact that documents its lifecycle precisely — states, transitions, guards for "missed," "rolled over," "completed late," etc. | After the rollover/routine design session |
| 3 | **Class diagram / CRC cards** | Encode the outcome of the template-system decision (inheritance vs. composition) as a concrete class structure | After the template-system design session |
| 4 | **ER diagram** | Database schema, derived from the class model once entity/attribute boundaries are settled | After class diagram |
| 5 | *(Deferred)* Sequence diagrams | Only for specific complex interactions (e.g., alarm scheduler triggering across the rollover boundary) once that logic exists to describe | Stage 5+ as needed |
| 6 | *(Deferred)* Deployment diagram | Not useful until sync (Stage 8/9) makes multi-node deployment real | Stage 8+ |
| 7 | *(Deferred)* Activity/swimlane diagrams | Only if a specific workflow (e.g., AI-extraction-to-review pipeline in Stage 11) benefits from explicit flow modeling | Stage 11 |

### 2.2 Why this ordering, and why not "draw everything now"

Pressman's requirements-modeling material (SE2, Doc 5) lists five categories of analysis element: scenario-based, class-based, behavioral, data, and flow-oriented. Producing all of them immediately would front-load documentation cost onto a system whose two central design questions aren't resolved yet — any class or ER diagram drawn before those decisions would need to be redrawn, and worse, the act of drawing a class diagram tends to implicitly force an inheritance-vs-composition answer through the diagramming notation itself. That's precisely the shortcut being avoided by resolving the open questions first, in a dedicated session, on their own terms.

The state diagram is placed early and deliberately *after* the rollover decision rather than as a tool to reach it — its job here is to document the decided lifecycle precisely enough to catch edge cases (what Pressman's requirements-validation checklist calls "areas where clarification may be required"), not to be the venue where the decision itself gets made under diagramming pressure.

---

## 3. Technology Stack Rationale

*(Captured from prior design discussion, not re-derived here.)*

| Decision | Choice | Reason |
|---|---|---|
| NLP/AI integration | Existing LLM API, not a custom engine, with a **mandatory human-review step** before AI-extracted data is committed to the database | Building a custom NLP engine is out of scope for a solo project; the review gate protects data integrity — directly serving the second core problem statement (routine data shouldn't be silently corrupted), this time against AI extraction errors rather than retroactive completion |
| Deployment | React Native first, full native rewrites (Kotlin, Swift) once feature set stabilizes | Speed to a usable, testable increment matters more early on than platform-native performance; rewriting after stabilization avoids optimizing a design that's still changing |
| Monetization | Fully free at launch; possible future B2B licensing | Keeps early focus on solving the personal problem the app was built for, rather than building monetization infrastructure against unknown market needs — flagged as a known tension with the personal-project framing, not yet resolved |
| v1 scope | Backend-first: alarm scheduler, rollover system, incremental routines, basic task management | These are the systems where the app's actual differentiation lives (per prior analysis, rollover/routine handling is a stronger differentiator than date separation alone); frontend polish, social features, and analytics are deferred because they don't test the core hypothesis |
| UI | Simple/Advanced toggle sharing business logic, separate presentation | Serves both casual and power users without duplicating the data layer — though this doesn't eliminate the cost of maintaining two presentation states per screen, which is tracked as a known ongoing cost, not a free abstraction |

---

## 4. Open Items Before Proceeding

These block Section 2's diagram sequence and should be resolved next, in order:

1. **Rollover + incremental routine interaction on a missed day** — stacked duplicate vs. independent miss-and-regenerate. Blocks the state diagram and the data model underneath it.
2. **Template system architecture** — OOP inheritance from an Abstract Task Class vs. composition/schema-driven dynamic attributes. Blocks the class diagram and ER diagram.

Both are scheduled for a dedicated grill-me session, separate from diagramming, per the plan above.
