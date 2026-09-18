# Dotick — Future AI Agent & Generative Experience Vision

> **Status:** Confirmed Future Product Direction  
> **Scope:** Future capability; **not** a Personal V1 implementation requirement  
> **Purpose:** Preserve the product decisions and architectural boundaries for a future built-in AI Agent and AI-generated experience layer without forcing their runtime implementation into current increments.

---

# 1. Vision

Dotick may evolve from a conventional productivity application into a **personal productivity environment with a stable product kernel and a user-specific generative experience surface**.

The future system has two distinct AI roles:

1. **AI Agent** — may inspect and, within User-granted authority, act on Dotick data through the same product capabilities available to ordinary clients.
2. **AI Experience Designer** — may generate or adapt how Dotick looks and how the User reaches supported actions, while preserving the meaning, validation, authorization, and integrity of those actions.

These roles must not become independent sources of truth for Dotick domain state.

The governing invariant is:

> **Generated experiences may redefine how Dotick looks and how Users reach an action, but they may never redefine what that action means.**

A Task remains a Task, completion remains the canonical Task-completion operation, authorization remains authoritative, and persistent state remains governed by Dotick even when the visible interface is radically different.

---

# 2. Stable Product Kernel

The future AI layers sit above the existing Dotick core rather than replacing it.

The stable kernel owns at least:

- domain entities and invariants;
- persistence and synchronized state;
- authorization and effective access;
- validation and business rules;
- recurrence and time semantics;
- history, audit, Trash, restore, and Undo semantics;
- collaboration semantics;
- command/use-case meaning;
- data-integrity safeguards.

AI-generated presentation or Agent execution must not bypass these boundaries.

Conceptually:

```text
AI Experience Designer               Built-in AI Agent
          |                                  |
          v                                  v
Experience Specification          Agent Capability Gateway
          |                                  |
          v                                  v
Experience Safety Runtime ------> Registered Product Actions
                     \                /
                      \              /
                       v            v
                         DOTICK CORE
                             |
                             v
                    Authoritative State
```

The exact implementation may differ, but the separation of responsibility must remain.

---

# 3. Generative Experience Layer

## 3.1 User-controlled transformation distance

The User chooses how far a generated experience may depart from the existing Dotick interface.

The confirmed conceptual levels are:

### Level 1 — Recolor

May change primarily:

- colors;
- material treatment;
- typography and related visual tokens.

The existing layout and interaction model remain substantially unchanged.

### Level 2 — Restyle

Includes Recolor plus changes such as:

- icons;
- component visual treatment;
- backgrounds;
- decorative language;
- borders, surfaces, and related styling.

The recognizable product structure remains substantially unchanged.

### Level 3 — Transform

Includes Restyle plus changes such as:

- motion and transitions;
- micro-interactions;
- sounds where supported and permitted;
- component presentation and shape;
- interaction metaphors that still resolve to the same Dotick capabilities.

For example, creating, completing, or deleting an Item may use a theme-specific animation while the underlying operation remains the ordinary Dotick operation.

### Level 4 — Reimagine

May additionally change:

- page/layout composition;
- navigation presentation;
- arrangement of controls;
- interaction patterns;
- visual representation of productivity concepts.

Reimagine may make Dotick look substantially different from the default interface, but required capabilities must remain reachable and the core product semantics must remain unchanged.

The User may also express narrower constraints in natural language, such as preserving the current layout while changing only visual style.

---

## 3.2 Declarative Experience Specification

AI-generated experiences must be represented through a **constrained declarative Experience Specification/DSL** interpreted by Dotick.

The AI must not be allowed to ship unrestricted executable client code as a theme. In particular, a generated experience must not require Dotick to execute arbitrary AI-generated JavaScript, React code, native code, or unrestricted CSS in order to function.

Instead, the future Experience Specification may describe registered concepts such as:

- design tokens;
- typography;
- colors and materials;
- layout primitives;
- registered components;
- component composition;
- motion and transitions;
- sounds;
- gestures;
- responsive rules;
- data bindings;
- conditional presentation;
- state-dependent visuals;
- mappings from an interaction to a registered Dotick capability/action.

Illustrative, non-normative example:

```json
{
  "component": "task-card",
  "variant": "block",
  "enterMotion": "drop",
  "completeMotion": "line-clear",
  "actions": {
    "primary": "task.complete",
    "delete": "task.trash"
  }
}
```

`task.complete` and `task.trash` are interpreted by Dotick. The Experience Specification does not redefine their business meaning.

The exact DSL/schema, renderer, primitive catalog, and serialization belong to future Design.

---

## 3.3 Generated behavior is presentation behavior

A generated experience may alter selected interaction behavior when that behavior remains within the Experience Runtime boundary.

Examples include:

- animation used when an Item is completed or removed;
- the visual way a new Task enters a view;
- drag/drop feedback;
- theme-specific completion effects;
- visual progress metaphors;
- navigation presentation.

The generated layer may not redefine:

- whether an operation is authorized;
- what makes a Task complete;
- recurrence meaning;
- sync/conflict semantics;
- deletion/retention semantics;
- persistence invariants;
- domain validation;
- security boundaries.

---

## 3.4 Generation is not in the ordinary interaction loop

The LLM is not required for every click, drag, completion, navigation action, or render.

The intended lifecycle is hybrid:

```text
User request
    ↓
AI generates or edits Experience Specification
    ↓
Validation / repair / preview
    ↓
User applies version
    ↓
Normal interactions execute locally through the Experience Runtime
```

The AI is invoked again when the User requests regeneration, editing, adaptation, or another supported design operation.

This preserves responsiveness, predictable behavior, offline usability of an already-applied experience where practical, and controlled AI cost.

---

# 4. Experience Validation and Safety Pipeline

An AI-produced Experience Specification must not be trusted solely because a model produced it or because another model says it looks correct.

The intended future pipeline is:

```text
AI Generate
    ↓
Deterministic Structural Validation
    ↓
Automatic Repair where safe
    ↓
Functional Simulation
    ↓
Accessibility Validation
    ↓
AI UX Review
    ↓
Interactive Preview Sandbox
    ↓
User Apply
```

A failed validation may cause deterministic repair, AI-assisted repair/regeneration, or rejection. An invalid experience must not be applied merely because it renders.

## 4.1 Structural validation

Deterministic validation should verify matters such as:

- schema validity;
- registered component/primitives only;
- registered product actions only;
- valid ranges and values;
- valid navigation destinations;
- responsive-rule validity;
- required capability availability;
- no forbidden execution surface.

These checks should not consume LLM tokens when deterministic validation is sufficient.

## 4.2 Capability contracts

Future UI surfaces may define **capability contracts** for important workflows.

For example, a List experience may be required to preserve reachable ways to:

- inspect the List;
- create a Task;
- open a Task;
- complete a Task;
- reach List management actions;
- navigate away from the view.

The AI may change how these capabilities are presented, but it must not make required functionality unreachable.

Exact contracts belong to the future Experience specification and owning UI/UX design.

## 4.3 Functional simulation

Before Apply, the generated experience should be exercised against a synthetic Dotick workspace containing representative states and edge cases.

Automated journeys may include, where applicable:

- navigate between primary surfaces;
- create an Item;
- open and edit an Item;
- complete an Item;
- delete and Undo;
- move/drag an Item;
- search;
- use empty/error/loading states;
- reach Settings/recovery controls.

This simulation changes only synthetic data.

## 4.4 Accessibility validation

The generated-experience release must define a measurable accessibility baseline before the capability becomes production-ready.

The generator and validators should prevent violations before Apply through deterministic checks and automated accessibility tooling where possible, including applicable checks for matters such as contrast, text scaling, focus behavior, target size, semantics, and motion/reduced-motion behavior.

Automated checks are not assumed to detect every accessibility issue. AI review and User preview complement deterministic tooling; they do not replace it.

The exact standard/version/conformance level remains owned by the future mature/public accessibility specification and is not introduced retroactively as a Personal V1 requirement by this document.

## 4.5 AI UX review

After deterministic correctness checks, an AI reviewer may evaluate concerns that are difficult to encode as strict rules, such as:

- understandable visual hierarchy;
- confusing interaction patterns;
- coherence between requested concept and resulting interface;
- discoverability;
- whether the product still reads as a usable productivity environment.

AI UX review is advisory/repair-oriented and is not the only safety gate.

---

# 5. Interactive Preview Before Apply

A newly generated or newly adapted experience must be previewable in a **fully interactive sandbox using synthetic/prebuilt Dotick data** before it becomes the active experience on that device.

The Preview is not merely a screenshot. The User should be able to move through representative Dotick surfaces and exercise important interactions without modifying real Account data.

The preview environment may expose actions such as:

- navigate views;
- create/edit/complete/delete synthetic Tasks;
- drag/move synthetic Items;
- inspect Calendar/Routine or other supported surfaces;
- observe animations, motion, sounds, and gestures;
- regenerate or edit the prompt/specification;
- Apply only after satisfaction.

The exact preview dataset and coverage are future Design details.

---

# 6. Experience Versioning, Recovery, and Sharing

Generated experiences are persistent/versioned artifacts rather than ephemeral model responses.

The system must preserve a reliable recovery path independent of the generated experience. Future Design must provide an always-reachable way to return to a known-good/default experience, for example through a protected recovery action or platform interaction. The generated experience itself must not be able to remove or redefine this recovery capability.

A previously working experience version should remain restorable after a new version is applied.

The User also intends generated experiences to be shareable through a controlled link/file/package mechanism. Shared experiences must still pass local validation before Apply. Sharing an experience does not grant authority to bypass Dotick safety checks.

Generated, User-provided, or externally sourced visual/audio assets may be supported in the future, but asset provenance, licensing/IP constraints, safety, caching, integrity, and trust rules must be defined in the owning future Design before external assets become a production capability.

---

# 7. Cross-device Experience Adaptation

A generated experience is **not automatically activated on every device** merely because it has been finalized on one device.

When a User creates or updates an experience on Device A, another device may notify the User that a new experience version is available. The User chooses whether to adapt it for that target device/form factor.

Conceptually:

```text
Existing Experience Specification
        +
Target device/form-factor capabilities
        ↓
AI adaptation
        ↓
Validation
        ↓
Target-device Preview
        ↓
User Apply
```

Adaptation should reuse the existing Experience Specification rather than regenerate the entire concept from scratch when practical.

One conceptual experience may therefore have device/form-factor-specific validated variants, for example Desktop and Mobile variants derived from the same parent experience.

This behavior reduces unnecessary AI generation cost and prevents an incompatible experience from silently replacing a working interface on another device.

---

# 8. Built-in AI Agent

## 8.1 Authority is User-selected

The future built-in Agent operates only within authority selected by the User. The intended UX exposes a small number of understandable authority profiles rather than requiring the User to configure a large low-level permission matrix for ordinary use.

The confirmed conceptual profiles are:

### Observe

The Agent may inspect permitted Dotick context but does not mutate product state.

### Ask

The Agent may prepare/propose mutations, but User confirmation is required before writes are applied.

### Assist

The Agent may execute low-risk actions within granted scope. Sensitive, destructive, or otherwise protected actions require confirmation according to the applicable product policy.

### Autonomous

The Agent may act without per-action confirmation within the capability scope explicitly granted by the User. Non-overridable domain, authorization, integrity, and safety constraints remain in force.

The exact operation classification and capability matrix belong to future Agent Design.

## 8.2 Grant duration

Where applicable, the User may grant Agent authority for one of these lifetimes:

- **Once**;
- **This session**;
- **Always** / persistent until revoked.

Persistent authority must remain revocable.

## 8.3 Capability gateway

The Agent does not receive a separate privileged mutation path merely because it is an AI capability.

Agent actions must pass through the same authoritative application/domain operation boundary that applies to ordinary User actions, including:

- authentication/actor identity;
- effective authorization;
- validation;
- domain invariants;
- transactional/atomic behavior;
- history/audit;
- synchronization semantics;
- Undo/recovery semantics where the operation is undoable.

The Agent must not directly mutate the database, bypass an application service, redefine an operation, or use a generated Experience Specification as an alternative business-logic engine.

## 8.4 Undo is origin-neutral

Undo of planning/productivity data is a Core behavior, not an Agent-specific compensation mechanism.

If an operation is undoable when performed by a User, the equivalent operation remains undoable when initiated by the Agent. The system may record the initiating origin/actor so History can distinguish a human-initiated action from an Agent-initiated one, but that origin must not produce different domain meaning.

## 8.5 Confirmation and safeguards

The User may configure confirmation behavior to the extent allowed by the selected authority profile and future Agent policy.

However, User-selected autonomy does not disable non-overridable safeguards required for authorization, data integrity, atomicity, protected destructive behavior, or other product invariants.

---

# 9. Relationship between Agent and Generated Experience

The Agent and the Experience Runtime are separate layers.

A generated UI may expose a different control, gesture, or metaphor for a supported action, but that interaction resolves to a registered Dotick capability.

The Agent may invoke that same capability within granted authority.

Conceptually:

```text
Default UI -----------\
Generated UI ----------> Registered Dotick Capability -> Domain Rules -> State
Built-in AI Agent ----/
```

No caller receives permission to redefine the capability itself.

This common boundary is the main architectural preparation required before the future features are implemented.

---

# 10. Late Future: Generated Extensions

A later phase may allow an AI-generated experience to introduce bounded extension-specific state or rules, for example a theme-specific progression metaphor that reacts to real Dotick activity.

This capability is intentionally **not** part of the initial Generative Experience Runtime.

Current architecture should reserve conceptual room for a future extension boundary such as:

```text
Extension State
Extension Events
Extension UI
Extension Rules
```

No general extension execution engine, arbitrary code runtime, or extension database model should be introduced merely to anticipate this capability now.

When this future phase is designed, extension behavior must remain sandboxed and must not become an alternate source of truth for core Task/Event/Routine or authorization semantics.

---

# 11. Current-scope Architectural Guardrails

The Agent Runtime, Experience Generator, Experience DSL, preview sandbox, and generated-extension engine are not required in Personal V1.

However, current implementation should avoid choices that make the confirmed future direction needlessly expensive to introduce later.

Current design should therefore preserve these seams where practical:

1. **Presentation-independent domain behavior** — UI components do not own domain truth or duplicate core business rules.
2. **Stable application actions/use cases** — important mutations pass through application/domain boundaries that future default UI, generated UI, and Agent callers can share.
3. **Authorization at the authoritative boundary** — permission is not inferred from which UI component initiated a request.
4. **Origin-neutral history and Undo** — history/recovery semantics do not depend on whether the eventual caller is default UI, generated UI, or Agent.
5. **Shared design primitives/tokens** — current themes should reuse a common component/token foundation rather than becoming separate applications.
6. **No premature future runtime** — do not add Agent tables, Experience DSL engines, or Extension State solely in anticipation of the future capability.

The goal is compatibility, not Big Design Up Front.

---

# 12. Future Design Gates

Before the built-in Agent becomes implementable, future design must finalize at least:

- capability classification and mapping for Observe/Ask/Assist/Autonomous;
- sensitive/destructive action policy;
- permission-grant persistence and revocation;
- session/Once/Always semantics;
- Agent audit/origin representation;
- confirmation UX and failure behavior;
- external-AI context/privacy implications.

Before Generative Experience becomes implementable, future design must finalize at least:

- Experience DSL/schema and versioning;
- registered primitive/component/action catalogs;
- capability reachability contracts;
- deterministic validator and repair rules;
- functional simulation journeys and synthetic dataset;
- accessibility acceptance baseline for the shipping release;
- AI UX-review contract;
- preview sandbox isolation;
- device/form-factor adaptation model;
- recovery/default-experience escape path;
- asset provenance/security/licensing rules;
- experience package/share format.

Before Generated Extensions become implementable, future design must separately define the extension state/event/rule sandbox and its security/integrity model.
