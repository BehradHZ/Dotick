# Dotick

**A productivity system for managing what you need to do, what you want to build into your life, and the progress that actually matters.**

Dotick brings **Tasks, Events, Routines, Goals, daily planning, collaboration, and meaningful progress tracking** into one coherent productivity experience.

Rather than treating task management, habit tracking, scheduling, motivation, and collaboration as disconnected problems, Dotick is designed around a unified model for everyday planning and long-term progress.

---

## Why Dotick?

Productivity usually spans more than a to-do list.

You may need to:

* manage Tasks and deadlines;
* keep track of Events and recurring schedules;
* build and maintain Routines;
* organize work across different areas of life;
* understand what you actually accomplished;
* stay motivated without turning productivity into a game;
* collaborate with other people when needed.

These needs are often split across several tools, each with its own model of time, progress, organization, and history.

**Dotick aims to bring them together without sacrificing depth, flexibility, or control.**

---

## What Dotick Covers

### Tasks & Events

Plan both scheduled and unscheduled work, manage deadlines and priorities, organize related work hierarchically, and keep Tasks and Events connected without forcing everything into the same lifecycle.

### Routines

Track recurring activities as continuing definitions rather than disposable daily tasks.

Each day can carry its own progress or outcome, including partial progress, completion, skipped intentions, historical corrections, and activity outside the expected schedule.

### Organization

Dotick uses a simple organizational hierarchy:

```text
Folder
└── List
    └── Column
```

Tasks and Events can be organized within this structure, while an Inbox provides a reliable default destination for newly created work.

### Recurrence & Reminders

Tasks, Events, and Routines can recur according to their own semantics rather than being forced through one universal recurrence model.

Dotick also supports reminders while keeping scheduling, recurrence, and recorded reality as separate concepts.

### Goals & Daily Rings

Dotick goes beyond storing work.

It can identify meaningful Goals from the User's activity and create **Daily Rings**: achievable daily plans intended to move those Goals forward.

Daily Rings focus on meaningful progress rather than simply rewarding the number of checked boxes.

### Meaningful Gamification

Streaks, progress, scoring, feedback, and other motivational mechanisms exist to reinforce productive behavior.

Gamification is a supporting layer—not the identity of the product.

Actual work and actual progress always remain more authoritative than game mechanics.

### AI-Assisted Creation

Dotick can turn spoken intent into structured Task, Event, or Routine proposals.

AI-generated results are reviewable and editable before they become real Items, keeping the User in control of the final state.

AI is an optional intelligent layer rather than a requirement for normal productivity management.

### Sharing & Collaboration

Dotick supports both direct person-to-person sharing and persistent Group collaboration.

Users can collaborate around Tasks, Events, Routines, Lists, and other supported Resources without forcing every shared interaction into a team or organizational workspace.

### Offline Use & History

Core productivity should not disappear when the network does.

Dotick is designed around offline-capable workflows, synchronization across devices, meaningful history, recovery, and traceability of important changes.

Historical corrections are supported without silently rewriting already finalized historical outcomes.

---

## Product Principles

### Productivity before gamification

Motivational systems must reflect real progress rather than manufacture it.

### Planned state and actual state are different

What was expected to happen and what actually happened are both valuable information. Dotick keeps those concepts distinct.

### Powerful without being unnecessarily complicated

Dotick is intentionally capability-rich.

Complexity should be managed through good context and presentation—not by removing useful capabilities simply to make the product appear minimal.

### Useful defaults, meaningful control

The product should work without extensive initial configuration while still giving users substantial control over their workflow.

### Truthful, traceable, recoverable

Important changes should remain understandable and recoverable. Convenience must not come at the cost of silently losing meaningful state or history.

### Offline-first core behavior

Normal productivity workflows should remain usable without continuous connectivity whenever the capability itself does not inherently require an online service.

### AI is optional

Core Task, Event, Routine, organization, and collaboration functionality must remain useful without external AI.

### Consistent semantics

Different clients and interfaces may present Dotick differently, but the meaning of the User's data and the rules governing it must remain consistent.

---

## Current Scope

Dotick is currently focused on **Personal V1**.

The scope includes personal productivity and non-organizational collaboration, including:

* Task, Event, and Routine management;
* organization and navigation;
* recurrence and reminders;
* history and recovery;
* offline use and synchronization;
* direct sharing and Group collaboration;
* AI-assisted Item creation;
* Goal discovery;
* Daily Rings, streaks, statistics, and adaptive motivational features.

The objective of Personal V1 is to establish the complete core Dotick experience before expanding into organizational use cases.

---

## Future Direction

Dotick is designed so its core model can evolve beyond Personal V1.

Potential future areas include:

* organizational and Enterprise workspaces;
* customizable organizational roles and permissions;
* organization-level administration and reporting;
* external productivity and calendar integrations;
* controlled automation through external assistants and agents;
* deeper platform-specific experiences and integrations.

These capabilities are intentionally separated from the current Personal V1 scope.

---

## Project Status

Dotick is under active development.

The product definition, major product decisions, formal requirements, and incremental development roadmap have been established. Development proceeds incrementally toward the Personal V1 baseline.

The project follows an iterative process in which requirements, design, implementation, testing, and validation evolve together while preserving the canonical product behavior.

---

## Documentation

The repository contains dedicated documents for different levels of the project:

* **[System Definition](project-docs/02-requirements/system-definition.md)** — what Dotick is, its scope, and its canonical product behavior.
* **[Decision Register](project-docs/decision-register.md)** — the reasoning, trade-offs, and constraints behind major product and domain decisions.
* **[Software Requirements Specification](project-docs/02-requirements/srs.md)** — formal and testable requirements for Personal V1.
* **[Development Roadmap](project-docs/01-planning/increment-roadmap.md)** — the incremental path from the engineering baseline to Personal V1 and future evolution.

For questions about current product behavior, the **System Definition is the primary authority**.

---

## Vision

Dotick is not intended to be just another to-do list, habit tracker, calendar, or productivity game.

The goal is to build a system capable of understanding the different kinds of work and commitments in a person's life, helping organize them coherently, preserving an accurate history of what actually happened, and providing enough structure and motivation to make meaningful progress every day.
