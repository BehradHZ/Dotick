# Dotick — System Definition

---

# 0. Document Purpose & Status

## 0.1 Purpose

This document defines what Dotick is, what is included within its Scope, and how the system behaves from the product and domain perspectives.

This document must describe the **current and finalized state of the system**, not the history of how decisions were made.

## 0.2 Canonical Status and Authority

This document is not a formally standardized artifact with a mandatory industry-defined name, such as an SRS. Within Dotick, it is used as an intermediate canonical document for defining the system, and the Formal SRS is subsequently derived from it.

If documents conflict regarding **product behavior or product Scope**, the order of authority is:

```text
System Definition
    ↓
Decision Register
    ↓
Formal SRS
    ↓
Domain Model / Design
    ↓
Roadmap / derived references
```

The `System Definition` is the primary authority for current-state behavior. The `Decision Register` preserves the rationale, trade-offs, and clarifications behind decisions and must not contain an active contradiction with the current behavior defined in this document. The `Formal SRS` converts the behavior defined here into testable requirements. The Roadmap only defines implementation order and implementation gates for this behavior; it has no authority to introduce new product behavior.

## 0.3 Relationship with Decision Register

A subject that requires a behavioral change or clarification may be analyzed in the `Decision Register` so that the problem statement, alternatives, trade-offs, and rationale are recorded. However, **current behavior becomes canonical only when it is reflected in the System Definition**.

After a decision is finalized:

- the `System Definition` is the primary authority for the current state and behavior of the system;
- the `Decision Register` preserves the rationale and boundaries of that decision in a form consistent with the System Definition;
- the `Formal SRS` derives testable requirements from that behavior.

## 0.4 Allowed and Disallowed Open Areas

At a high level of abstraction, the primary concepts, Scope, and overall system behavior must not remain ambiguous or unresolved.

Matters concerning **how the system is implemented** or **the exact mechanism used to achieve a required behavior** may remain unspecified or open in this document. Examples include:

- implementation strategy;
- storage strategy;
- physical schema;
- exact algorithm;
- exact scoring coefficients and formulae;
- technical details of how a target is achieved.

The expected behavior itself, and the product meaning of that behavior, must nevertheless be explicit.

## 0.5 What This Document Covers

- product definition and the problem it solves;
- Current Scope and Future Scope;
- relevant stakeholders and user classes;
- system context and system boundaries;
- product principles;
- functional capabilities at the behavioral level;
- high-level domain and business rules;
- system-wide behaviors;
- interaction with external systems;
- quality expectations and product-level constraints;
- assumptions and dependencies;
- glossary of domain-specific concepts.

## 0.6 What This Document Does Not Cover

This document is not the place for implementation details. The following belong in their respective specialized documents:

- SQL schema;
- table/index design;
- ORM mapping;
- implementation of class hierarchies;
- exact API endpoints;
- exact JSON payloads;
- UI components;
- wireframes;
- algorithm implementation;
- scoring coefficients;
- test cases;
- implementation order;
- Increments;
- deployment instructions;
- CI/CD;
- library/framework choices, unless a specific choice is itself a finalized product constraint.

## 0.7 Writing Rule

The primary writing rule for this document is:

> It must be technical enough that system behavior is unambiguous, but not so implementation-specific that it locks the implementation approach.

For every paragraph, reviewers can ask:

> If the entire backend were rebuilt tomorrow using a different technology, would this statement still have to remain true?

If the answer is yes, the statement probably belongs in the System Definition. If its truth depends on a PostgreSQL table, a REST endpoint, a framework, a component, or another implementation detail, it probably belongs in Design.

---

# 1. Product / System Overview

## 1.1 What Dotick Is

Dotick is a daily productivity-management service that allows a User to manage Tasks they intend to perform, Events that are upcoming, and Routines or habits they want to incorporate into their life.

In addition to these foundational behaviors, Dotick uses the User's Tasks, Routines, and other required activities to generate aligned daily Goals and applies appropriate Gamification to help the User make sustained progress toward a better version of themselves.

## 1.2 Problem Being Solved

A User who wants to manage daily planning seriously and consistently usually faces several needs at the same time: managing Tasks and Events, tracking Routines and recurring patterns, maintaining focus and motivation for meaningful work, and, in some situations, coordinating and collaborating with other people. When these needs are handled by separate tools or separate conceptual models, the User must distribute planning, activity history, progress state, and collaboration across multiple environments and therefore loses a unified view of daily work and Goals. Dotick is defined to reduce this fragmentation by bringing these related needs into a coherent model and a single experience, without allowing the motivational layer or collaboration capabilities to compromise the product's professional and practical nature.

## 1.3 Primary Product Value

Dotick's primary differentiating value is the integration, within one modern product, of capabilities that have traditionally existed as isolated features across separate task-management products.

Dotick simultaneously manages Tasks, Routines, and Events with correct recurrence semantics, uses Gamification to increase User motivation without reducing the product's professional character, and supports proper multi-user collaboration around a shared plan.

## 1.4 Main Usage Model

The User interacts with Dotick repeatedly throughout the day. This interaction may occur through any supported client provided within the product's Current Scope.

Because Dotick is intended for continuous daily use, supported clients must remain consistent with one another with respect to data, core behavior, Item state, and product rules. Differences caused by platform limitations or platform-specific capabilities may be expressed at the presentation layer or in OS-dependent capabilities, but they must not change the core meaning of domain data or domain behavior across clients.

## 1.5 High-level Capability Summary

Based on the problem and value defined in Sections 1.2 and 1.3, Dotick's primary high-level capabilities are:

- Task management;
- Event management;
- Routine and recurring-pattern management;
- Gamification and progress tracking while preserving the product's professional nature;
- multi-user collaboration and sharing within the defined Scope;
- a consistent experience across supported product clients.

The details of these capabilities are defined in Section 6, `Functional Capabilities`.

---

# 2. Scope & Boundaries

## 2.1 Current Scope

Within the Current Scope, Dotick is designed for personal use and collaboration in small, non-organizational groups.

## 2.2 Future Vision

Dotick is designed from the beginning so that, in the future, its core can support an organizational management product with company-specific customizable roles and access levels.

## 2.3 Current-Scope Boundary Summary

Within the Current Scope, Dotick covers personal use and non-organizational collaboration. Capabilities such as Groups, Comments, predefined roles, and direct collaboration between Users are within Current Scope provided that they do not depend on a hierarchical organizational model or arbitrarily customizable permissions.

Capabilities explicitly outside Current Scope or reserved for the future are defined only in Section 12 so that there is a single authoritative location for Out-of-Scope and Future Scope behavior.

## 2.4 Scope Boundary Rules

The primary criterion for including a capability in Current Scope is whether the current target User genuinely needs it for personal-life management or non-organizational collaboration. At the current stage, the founder is the `Product Owner`, the `primary target user`, and the final authority for product decisions.

The boundary between Current Scope and Future Enterprise Scope is not determined by the number of members in a Group or merely by the social relationship between those members. A capability enters Enterprise Scope when its behavior depends on formal organizational governance, including concepts such as `organization hierarchy`, `Custom Role` or arbitrary permission composition, `manager/subordinate visibility`, `Organization/Tenant`-level isolation, or management/reporting capabilities that depend on organizational structure.

Accordingly, non-organizational collaboration using Direct Sharing, Groups, predefined Access Profiles, and System-defined Roles may remain in Current Scope. Dotick does not define a fixed product-level numerical threshold at which a Group automatically becomes Enterprise. The fact that Group members happen to belong to a company is also insufficient by itself to classify that Group as Enterprise; the determining criterion is the need for organizational governance and authorization semantics.

---

# 3. Stakeholders & User Classes

## 3.1 Registered Personal User

Within Current Scope, every registered Dotick account is fundamentally a `Registered Personal User`. A User does not become a separate account type in order to use collaboration capabilities, and joining a Group or receiving access to another Resource does not remove or replace the personal capabilities of that User's account.

A Registered Personal User can:

- create and manage their own personal Resources;
- Share their shareable Resources with other Users;
- manage or revoke granted access within the limits of their own permissions;
- view or act on Resources Shared by other Users according to their effective access;
- create one or more Groups;
- become a member of one or more Groups.

Resource ownership, access to that Resource, and responsibility for performing a Task are three independent concepts. Being in one of these states must not implicitly create either of the other two states.

Creating an Account is a mandatory prerequisite for using Dotick. Anonymous or guest application usage is not supported. Every Registered Personal User must have a unique username/handle. For Direct Sharing and Group-invitation discovery, registered Users may be found through username/handle, supported name/Display Name search, email, or phone. Discovery only identifies the intended collaboration recipient; discovery alone does not create access or Membership.

Each User may have an optional `Profile Picture`. The Profile Picture is part of the Account's identity presentation and may be displayed together with Display Name and username/handle in contexts where the User's identity is legitimately shown, such as collaboration discovery results, Share/Group requests, Member lists, Comments, and Assignments. This capability does not create a Public Profile, a social graph, or an independent public-discovery surface.

An invitation to a Resource or Group may be initiated through an invite link or by recipient discovery using username/handle, name, email, or phone. The invitation becomes actual access or Membership only after the recipient authenticates or registers with a valid Account and completes the relevant acceptance flow.

## 3.2 Direct Collaborator

`Direct Collaborator` is not a separate user class or account type. It describes an **access context** in which a Registered Personal User has been granted direct access to a specific Resource.

A Direct Collaborator's access level is determined independently for each Resource and may be constrained through predefined Access Profiles. Therefore, the same User may simultaneously own their own personal Resources, have view-only access to another Resource, and have Comment or edit permission on another Resource.

Direct access to a Resource does not by itself create GroupMembership.

## 3.3 Group Member

`Group Member` is also not a separate account type. A Registered Personal User acts as a Group Member within the context of a Group of which they are a member.

Each GroupMembership in Current Scope has a `System-defined Role`. That Role defines the User's capability range within the Group context, but the User's final access to any specific Resource must still be consistent with the authorization rules that apply to that Resource.

A User may belong to multiple Groups simultaneously, and their role or access level in each Group is independent from their role or access in other Groups.

Every Registered Personal User may create a new Group. At the moment of Group creation, the creator automatically receives full Collaboration-Management Permission for that Group, represented by the Manager role, and initially holds all management capabilities for that Group.

Joining an existing Group always requires confirmation by the joining User and cannot be imposed unilaterally by the Group. Joining may occur through either of these paths:

- the User opens a received invite link using their Account and confirms it;
- a holder of Collaboration-Management Permission finds the intended User through discovery by username/handle, name, email, or phone and sends that User a membership request.

In both paths, the intended User receives a Notification and may accept or reject the request. In Future Enterprise Scope, even if a superior directly initiates adding a member to a Group, the addition still remains conditional on acceptance by that member through the corresponding Notification.

Leaving a Group depends on the Group context:

- in non-organizational Groups within Current Scope, a Group Member may leave immediately at any time without requiring anyone else's approval;
- in Future Enterprise Scope, a member may not leave a Group unilaterally. The member may only submit a leave request, and the Membership ends only after approval by the relevant superior, such as a team manager.

## 3.4 User with Collaboration-Management Permissions

A User who has been granted management permissions within a Direct Share or Group may perform the allowed management operations within that context, such as managing Sharing, Membership, or shared structure, provided that the corresponding capability has been granted.

This status does not by itself make the User a `Platform Administrator` or `System Administrator`. Management authority derived from Direct Sharing or GroupMembership is **scope-dependent** and valid only within the relevant Resource or Group. This is separate from the global Platform/System Administrator role used to administer the Dotick platform itself.

Within Current Scope, these permissions are provided only through predefined Access Profiles and predefined System-defined Roles. Custom Roles and arbitrary permission composition belong to Future Enterprise Scope.

A Group must always contain at least one member with Collaboration-Management Permission, i.e. a Manager. A Group must never be left with no Manager.

If the last or only Manager of a Group wants to leave, that Manager must designate another member as the new Manager before leaving. The departing Manager must be able either to select a specific eligible member directly or to choose a Random Assignment option among eligible members. The Manager cannot leave the Group until this succession has been completed.

## 3.5 Future Enterprise User

In Future Enterprise Scope, a Registered User may operate within an `Organization/Tenant` context in addition to personal and Group contexts.

An Enterprise User may be governed by rules such as organization hierarchy, Custom Roles, manager/subordinate visibility, or other organizational policies. These capabilities must not make the baseline Personal User behavior or the simpler Current-Scope collaboration model dependent on organizational hierarchy.

## 3.6 Other Relevant Stakeholders / Actors

At the current project stage, the primary product stakeholder is the founder User, whose real usage defines and evaluates the needs of Personal Scope and current collaboration behavior.

`Platform Administrator` / `System Administrator` is a global actor distinct from Registered Personal User, Direct Collaborator, Group Member, and Group Manager. This actor exists for administration and operation of the Dotick platform itself, and its authority is not derived from a Resource or Group Role or Access Profile. A Platform/System Administrator has unrestricted system-wide authority and, within an administrative context, may access all system data and state and perform any necessary administrative or corrective operation on Accounts, Resources, configuration, and other Dotick components. This global authority must not be treated as equivalent to the permissions of ordinary Users or Group/Sharing Managers; those permissions continue to derive only from their respective Resource or Group contexts.

External services, authentication providers, AI providers, and future integrations may be external actors of the system, but they are not human Dotick user classes. Their responsibilities are defined in the System Context and External Systems & Integrations sections.

---

# 4. System Context

## 4.1 System Boundary

Within Current Scope, the Dotick system boundary includes all components controlled by Dotick that are required to deliver the product's core behavior. This boundary is not limited to the backend; it includes the supported official clients, the local state required for Offline operation, the backend and internal API, server-side persistence, domain and business logic, internal authentication/account state, authorization, collaboration, sync, notification orchestration, and AI orchestration.

Within Current Scope, operational data for Task, Event, Routine, Goal, Group, Sharing, and other product capabilities is created or changed through Dotick's own clients. At this stage, Dotick does not import or synchronize productivity data from services such as Google Calendar, Notion, or TickTick.

The local copy of data on a device is not merely a read-only cache. Each device may maintain a valid, editable replica of the User state required for supported Offline flows. After connectivity is restored, local changes are reconciled with the server, and the valid synchronized result must then be made available for synchronization across the User's other devices. The exact conflict-resolution mechanism and sync metadata are determined in the relevant Design artifacts.

Within Current Scope, Dotick does not provide a public, general-purpose API for arbitrary external clients. If external access to an Account is later provided to external agents or assistants, that access is a controlled, permission-based integration within Future External Integrations.

## 4.2 Internal Responsibilities

Dotick is responsible for every behavior that determines product meaning, including:

- maintaining internal Account identity and state, and product data state;
- persistence and retrieval of operational data;
- enforcing the defined domain rules, lifecycles, and business rules;
- internal authentication flows, session handling, and mapping external identity assertions to internal Accounts;
- authorization and calculation of effective access for Personal, Direct Sharing, and Group Collaboration contexts;
- execution of Task, Event, Routine, Recurrence, Reminder, Goal, Daily Ring, Dotick Day, Statistics, History, and other Current-Scope behaviors;
- creating and maintaining the local replica required for Offline behavior, recording local changes, reconciling them with the server, and propagating the final synchronized state to the User's other devices;
- determining each Notification's trigger, recipient, timing, and content, and requesting delivery through the appropriate channel;
- complete orchestration of AI capabilities, including preparing context, constructing prompts, selecting an available provider, sending requests, receiving responses, validating and interpreting structured output, and applying product rules to the result;
- supporting default AI execution through service-managed providers/credentials and, when the User enables personal-credential mode, using that User's personal API/credential for a supported provider;
- preserving the core semantics and state of the product consistently across all officially supported clients.

Dotick must provide a complete global administrative context for the `Platform Administrator` / `System Administrator`. The Admin interacts with this management capability as a human actor outside the System Boundary and, while acting within the administrative context, may access all Accounts, Resources, states, and configuration in Dotick and perform any necessary operation on them. This authority is a platform-level administrative bypass and is not derived from a Group Role, an Access Profile, or a Resource permission.

## 4.3 External Responsibilities

External systems are responsible only for the specific capability delegated to them by Dotick. They must not be treated as the source of truth for Dotick domain behavior or internal authorization.

### AI Model Provider

AI models themselves are outside the System Boundary. Training or hosting a foundation model directly by Dotick is not a Current-Scope requirement. Instead, Dotick sends the context and prompt required for a specific task to an external provider and receives the response in the expected form.

The provider is responsible for running inference and returning a response. Dotick is responsible for deciding what data is sent, how the prompt is constructed, which provider is used, what response schema is expected, how that response is validated, and how the validated result is used in product behavior.

By default, Dotick selects an appropriate provider/model based on available providers and service policy; the User does not select the service-managed provider or model. A User may enable their own credential/API for a supported provider and may return to the default service-managed mode at any time. If the personal credential is unusable at request time, Dotick may continue the same request using its default service and must inform the User of that fallback in a non-blocking manner without requiring a separate popup. The provider catalog, credential storage/protection, and routing among service-managed providers are Design details. The fallback principle from a personal credential to the Dotick-managed service is finalized product behavior.

### Authentication Provider

Within Current Scope, Google is the only supported external authentication provider. Google is responsible only for the external authentication flow and for providing the identity assertion needed to prove identity. Dotick maintains the internal Account, username/handle, email/phone discovery state, product data, authorization, GroupMembership, Sharing state, and all other application state.

Google must not be the product's only authentication method. Email/password and Passkey remain independent Dotick authentication paths. However, a User who uses Google is not required to configure an independent fallback before using the Account. Dotick must allow the User to add an independent fallback and must recommend doing so. Consequently, a Google outage may temporarily prevent a new login for an Account that has no fallback configured, but it must not unnecessarily make existing data in a valid Offline session unusable.

### Notification Delivery Infrastructure

Dotick is responsible for Notification logic, while final delivery may depend on platform capabilities and push/OS-notification infrastructure. The operating system or delivery service is responsible for delivering and displaying a Notification within that platform's capabilities and policies. Dotick remains responsible for the Notification's meaning, the time at which delivery is requested, the recipient, and its content.

### Future External Integrations

Productivity and calendar services such as Google Calendar, Notion, TickTick, and similar systems are not Dotick data sources within Current Scope. Import, synchronization, or automation based on such systems belongs to Future Scope.

External AI agents and voice assistants that may later act on a User's Account with the User's explicit authorization are also external actors. They must interact only through a controlled, authorized integration surface. This does not imply exposing Dotick's backend as a public general-purpose interface to arbitrary external clients.

## 4.4 Context Overview

```text
Registered Personal User                          Platform / System Administrator
├── Personal Use                                  └── Unrestricted system-wide administration
├── Direct Collaboration                                      │
└── Group Collaboration                                       │
        │                                                     │
        └──────────────────────────┬──────────────────────────┘
                                   ▼
┌──────────────────────── Dotick System Boundary ───────────────────────────────┐
│                                                                               │
│  Official Dotick Clients                                                      │
│  ├── User Interaction                                                         │
│  ├── Local Operational Replica                                                │
│  └── Offline Changes                                                          │
│            │                                                                  │
│            ▼                                                                  │
│  Backend / Internal API                                                       │
│  ├── Domain & Business Logic                                                  │
│  ├── Account / Authentication State                                           │
│  ├── Authorization & Collaboration                                            │
│  ├── Platform Administration                                                  │
│  ├── Offline Sync & Reconciliation                                            │
│  ├── Dotick Day / Daily Rings / Statistics                                    │
│  ├── Notification Orchestration                                               │
│  ├── AI Orchestration                                                         │
│  └── Server-side Persistence                                                  │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
        │                         │                         │
        │                         │                         │
        ▼                         ▼                         ▼
Google / External          External AI Model        OS / Push Notification
Identity Provider          Provider(s)              Infrastructure

Future External Integrations
├── Google Calendar / Notion / TickTick / other productivity systems
├── User-authorized external AI agents
└── External voice assistants
```

---

# 5. Product Principles

## 5.1 Capability-rich Product with Intelligent UX

Dotick is intentionally designed as a **feature-rich** and customizable product. The goal is not to remove capabilities merely to produce a superficially simple UI. Instead, complexity must be managed intelligently so that each capability is available in the appropriate context and at an appropriate level of visibility.

The user interface may use context-aware presentation, progressive disclosure, appropriate information hierarchy, and workflows tailored to the User's level of need. This principle does not require displaying every action simultaneously, nor does it justify excessively hiding capabilities.

If artificial interface simplicity conflicts with meaningful flexibility for a power User, meaningful flexibility has higher priority. Internal backend or domain complexity should be exposed in the UI only when that distinction has independent value or meaning for the User.

## 5.2 Usable Defaults, User Control, and Adaptive Personalization

Configurable Dotick capabilities must have reasonable defaults so that using the system does not require mandatory initial configuration. At the same time, the User must be able to adjust customizable behavior to fit their workflow.

Where personalization or adaptation is part of product behavior, the system may use observed User behavior and preferences to adapt suggestions, defaults, difficulty, targets, or other permitted behaviors over time. Whenever an explicit User setting and an inferred preference control the same subject, the User's explicit choice is authoritative.

Adaptation must not remove User control. Motivational capabilities must also remain within a reasonable range: ordinary success must remain realistically achievable, while high-level achievements may remain challenging.

## 5.3 Truthful, Traceable, and Recoverable State

Dotick must distinguish between **what was planned to happen** and **what actually happened**. When a valid action has actually occurred, or when the User needs to correct historical data, recording reality takes precedence over artificially preserving the previous plan.

Schedule, recurrence, deadline, and other planning rules may affect suggestions, scoring, streaks, or consequences, but they must not erase or distort a valid recorded fact.

Meaningful changes to persistent domain data must remain sufficiently traceable to support history inspection, recovery, and conflict investigation. Current state may be updated or deleted when required, but the history necessary to understand that change must not silently disappear.

Some of this history may be exposed to the User in the UI, while not every internal audit detail must be user-facing.

When a real trade-off exists between a simpler implementation and better preservation of data, the solution with the lower risk of data loss has priority.

## 5.4 Additional Principles

### 5.4.1 Offline-first Core Behavior

Continuous network connectivity must not be a prerequisite for using Dotick's core productivity flows. Within the scope of supported capabilities, each device must be able to maintain a local editable replica.

After reconnection, local changes must be reconciled with the server. The server is the central synchronization point and must converge replicas to a final state and make that final result available for synchronization to the User's other devices.

Capabilities that inherently require an online service, such as AI inference, may be unavailable when there is no network connection or when the required provider is unavailable. Such unavailability must not disable core flows that do not depend on those services.

### 5.4.2 Productivity Truth over Gamification

Gamification is a supporting layer for productivity and must not turn Dotick's primary identity into a standalone game.

Motivational messages, behavioral pressure, streaks, achievements, and even critical or scolding messages may be part of the experience, but they must not distort actual progress or display more progress than actually occurred.

Whenever increased engagement conflicts with accurate representation of real progress, accurate representation has priority.

At the same time, after failure or falling behind, the system must preserve a real and meaningful path for the User to return to the desired trajectory. Failure must not make continued effort pointless.

### 5.4.3 Optional Intelligent Layers

AI, personalization, and recommendation are tools used for specific Dotick capabilities and are not prerequisites for core Task/Event/Routine management.

The User must be able to disable intelligent or personalized layers that are designed to be optional and continue using Dotick as a conventional productivity manager. In addition to feature-specific controls, there must be a global control that disables external AI processing. When external AI processing is disabled, AI-assisted Item Creation, Goal Discovery/AI Tag processing, and Daily Ring capabilities that depend on AI are disabled, while core Task/Event/Routine management, organization, collaboration, and other AI-independent behaviors remain usable.

For capabilities whose nature is inherently algorithmic or AI-based, disabling the intelligent layer may disable that capability itself. Dotick is not required to provide a manually equivalent workflow inside a capability that is intrinsically algorithmic.

AI authority is defined per capability. In flows where AI produces a reviewable proposal, that proposal must not be applied without User confirmation. In contrast, AI-managed capabilities such as semantic Goal discovery and the lifecycle of AI Tags may operate automatically according to their own defined rules.

### 5.4.4 Measured Responsiveness

Dotick must remain as fast and responsive as reasonably possible during ordinary daily interactions.

Feature richness is preserved by default. However, if measurement or practical validation demonstrates that a heavy behavior causes noticeable User-facing performance degradation, simplifying, deferring, asynchronously executing, or removing that specific behavior may be justified.

Performance optimization must not be based only on assumptions and must not be used as a pretext to remove capabilities prematurely. Trade-offs must be supported by actual evidence.

### 5.4.5 Future Evolution and Technology Replaceability

Current-Scope design must not unnecessarily block future product evolution. Accepting a reasonable amount of structure or complexity in the current design is permitted when it clearly reduces future development, migration, or expansion cost.

Core domain semantics must not be tied to a specific framework, provider, client, or technology unless such dependency is genuinely required. Technology-specific dependencies should, to a practical extent, remain contained within explicit boundaries.

The goal is **bounded coupling and practical replaceability**, not unnecessary abstraction based on the assumption that every technology must be replaceable at zero cost.

Accordingly, even when the full implementation of a cross-cutting capability belongs to a later Increment, foundational decisions in earlier Increments must remain compatible with the future semantics already known to the project. In particular, early Data/API/identity/version/delete/order decisions must be reviewed against Offline/Sync, branching History/Audit, authorization/revocation, and Time Semantics requirements so that introducing a later capability does not unnecessarily require breaking the foundational model.

### 5.4.6 Explicit Scope for Sharing Actions

Sharing a container may extend access to its descendants.

Whenever an action expands inherited access across multiple Resources, the system must show the initiating User the scope of the effect in an understandable form and obtain explicit confirmation before applying the change.

This confirmation is independent of recipient-side acceptance and exists to prevent accidental exposure of descendant Resources.

### 5.4.7 Consistent Semantics across Clients

Different Dotick clients may have different presentation, interaction, and platform-specific capabilities, but shared domain data semantics and shared business behavior must not vary by client.

Native or platform-specific capabilities are permitted as long as they do not change the system's core semantics.

---

# 6. Functional Capabilities

> This section must be organized by capability/domain, not by database table or class implementation.
>
> For each capability, this section defines the expected behavior, rules, lifecycle, important edge cases, and interactions with other capabilities. Implementation, storage, schema, endpoint, and exact algorithm details are not defined here unless they are necessary to define product behavior.

## 6.1 Information Organization

Dotick's primary information-organization hierarchy is:

```text
Folder
└── List
    └── Column
        └── Item
```

A `Folder` is an optional container in the User experience. A `List` may be visible without a Folder. If the implementation uses a hidden default Folder to keep the internal model uniform, that implementation detail must not force the User to see or manage that Folder in the UI.

Every Registered Personal User has a dedicated `Inbox`. The Inbox is a real, special List and is the default destination for Item creation. The User cannot delete or rename the Inbox.

At any given time, every Task and Event belongs to exactly one List and exactly one Column within that List. When a Task/Event is created, the default List is the Inbox; operationally, the User therefore always has a destination List. If the Task/Event is not created directly from a specific Column, the destination List's default Column is used. Routine does not use Folder/List/Column placement and is managed in the dedicated Routine space.

Folder, List, and Column may be manually reordered. Their titles are not required to be unique; multiple containers with the same title are valid.

Before a Column is deleted, the system must ask the User what should happen to the Items inside it. The User may either delete those Items together with the Column or move them to the default Column of the same List.

Deleting a List places all of that List's contents into the same deletion flow. Deleting a Folder likewise includes all Lists and their contents in the same deletion flow. Ordinary deletion follows the system's Trash and recovery rules.

Within Current Scope, the organization hierarchy contains only these three levels. Nested Folders and nested Columns are not part of the current model.

---

## 6.2 Task Management

A Task may be scheduled or unscheduled. A date/time is not required to create a Task. If a date is set but no time is set, the Task is treated as an all-day Task.

The primary temporal fields of a Task are `due_at`, `end_at`, and `deadline_at`. If a deadline exists and the User does not specify a grace period, the default grace period is zero. Valid temporal ordering must satisfy:

```text
due_at <= end_at <= deadline_at
```

When `end_at` is absent:

```text
due_at <= deadline_at
```

The recognized Task states are:

```text
Todo
Overdue
Missed
Done
Won't_Do
Skipped
```

Active time-driven transitions occur according to the defined Task lifecycle. Merely opening, viewing, or editing an old Task must not unintentionally re-evaluate its status. If a Task is already in a final or historical state, its status changes only through explicitly defined behavior or a User action; viewing the Item alone does not change its state.

`Skipped` remains a time-driven state and the User does not need to select it directly. However, the User may move a Task that the system previously transitioned to `Skipped` back into another permitted state.

### Dependency

A Task may depend on other Tasks. If Task A is blocked by Task B, Task A cannot become `Done` until Task B becomes `Done`.

Only `Done` satisfies a dependency. `Won't_Do`, `Skipped`, and all other states do not resolve the blocker.

If a blocker is deleted, the dependency relation to that blocker is also removed, and the dependent Task no longer requires that blocker.

Dependency cycles are prohibited. If a new dependency would create a cyclic chain, the system must reject that action and explain to the User that the new relation would create a cycle because of the existing chain.

Dependency is independent from hierarchy. Parent/Subtask structure does not implicitly create a dependency.

### Parent completion behavior

By default, when all structural children of a Task become `Done`, the Parent also becomes `Done`. The User must be able to disable this behavior in Preferences.

If the User directly marks a Parent as `Done`, all structural descendants of that Parent also become `Done`.

By default, this cascade applies only to `Done`. Time-driven states of a Parent must not change the states of its children.

By default, setting a Parent to `Won't_Do` does not change the state of its children. The User may enable an optional Preference that applies `Won't_Do` on a Parent to its structural descendants as well.

### Priority

Task Priority is one of:

```text
Urgent_Important
Important
Urgent
None
```

The User may change Task Priority throughout the Task lifecycle.

---

## 6.3 Event Management

An Event may be created, persisted, retrieved, and edited while completely unscheduled. Neither a start time nor an all-day date is required for the Event to exist. If a start date is specified without a time, the Event is interpreted as all-day. Schedule information may be added or completed later without replacing the Event or changing its stable identity.

While an Event is unscheduled, none of the time-driven statuses `Not_Arrived`, `Ongoing`, or `Finished` applies. Its time-driven lifecycle becomes meaningful only after a valid start schedule exists.

For a scheduled Event, the primary lifecycle is time-driven:

```text
before start              -> Not_Arrived
start <= now < end        -> Ongoing
after end                 -> Finished
```

If `end_at` is not explicitly set, the end of the Calendar Day associated with the start date is treated as the Event's end; after that point, the Event becomes `Finished`.

Event status is determined by time and is not manually changed by the User.

For an all-day Event, the selected Calendar Day in the effective scheduling timezone is converted into the real time interval representing that day. This interval is not the same as a Dotick Day. Once the interval is established, a later timezone change must not move its start/end instants; in another timezone, its local representation may therefore span parts of two Calendar Days.

Overlap between Events or other time-based Items is allowed. The system may warn the User about a time conflict, but overlap alone must not prevent creation or movement of an Event.

Event Priority uses the same set as Task Priority:

```text
Urgent_Important
Important
Urgent
None
```

For Daily Rings, an Event reaching `Finished` may satisfy the completion of the corresponding Daily Action, provided that the Action is eligible for credit in the current Ring.

An Event has at most one independent Location. A Location may be physical or virtual; its exact representation is defined in the relevant Design artifact.

---

## 6.4 Hierarchy & References

Task and Event may be structural children of one another. All of the following relations are valid at the domain level:

```text
Task  -> Task
Task  -> Event
Event -> Task
Event -> Event
```

Every Task and every Event has at most one structural parent. The domain does not impose a fixed maximum on the number or depth of structural descendants, although the UI is not required to render arbitrarily deep hierarchy inline. In tree views, presentation may directly display up to five levels and make deeper levels accessible through appropriate navigation.

Cycles in the structural hierarchy are prohibited.

When created, a structural child is placed in the same List and Column as its Parent. When the Parent is moved to another List or Column, its structural descendants move together with it.

The User may move a child independently to another location. If the new placement is incompatible with the structural Parent's placement, the parent/child relation is broken and the child becomes an independent Item.

Deleting a Parent also places its structural descendants into the same deletion flow.

Removing only the parent/child relation does not delete either Item. The Parent retains its other children, and the detached child retains its independent identity.

### References

A RichDescription may reference a Task, Event, or Routine. Goal is not referenceable inside Description within Current Scope.

A Reference does not create a structural relation, and the referenced Item may appear in multiple Descriptions simultaneously.

A Reference representation must be live. Changes to the referenced Item's title and current state must be reflected in that Reference. For entities without an independent status, only the states meaningful to that entity are displayed.

If a referenced Item is deleted, the Reference must not silently disappear. The Description must indicate that the referenced Item, identified by its last known title, has been deleted.

---

## 6.5 Description & Comments

Task and Event use a block-based RichDescription. Routine and Goal do not require the advanced RichDescription capability and may use a simpler description.

ContentBlocks have stable identity and may represent Text, Attachment, Location, or Item Reference content. A Comment targeting a block is associated with that block's stable identity.

### Comments on Task and Event

An authorized User may add a Comment either to the entire Item or to a specific ContentBlock. A Comment may be edited or deleted.

A deleted Comment disappears from the ordinary UI, but its creation, edits, and deletion remain traceable in Item history/audit.

A Comment may have replies. A reply must generate an appropriate Notification for the author of the target Comment.

A User may mention another User by username provided that the mentioned User is reachable within the relevant collaboration context, for example because the User belongs to the same Group or the Resource has been Shared with that User.

If a ContentBlock targeted by Comments is deleted, the Comments attached to that block are also removed from current state. However, the history of Comment creation and block/comment deletion remains preserved.

### Comments on Routine

Comments on a Routine are permitted for collaboration, but the Owner should not use Comments to record private personal observations about their own Routine. A User's personal experience or Note for a specific day must be recorded through the `RoutineCompletion` Note for that day.

If a Routine is Shared with another User, an authorized User may Comment either on the Routine as a whole or on the execution of a specific day.

---

## 6.6 Routine Management

A Routine is a single definition; the system does not create a separate Routine for every day. Each day's outcome or progress is recorded in the `RoutineCompletion` associated with that `occurrence_date`.

For each `(routine, occurrence_date)`, at most one current RoutineCompletion exists.

### RoutineCompletion state

A RoutineCompletion may have the following states:

```text
In_Progress
Done
Won't_Do
```

`In_Progress` is used when the User has recorded a measurable amount for a Routine but the applicable target has not yet been completed. Absence of a RoutineCompletion still means **no outcome or progress has been recorded** and is not equivalent to `In_Progress`.

For Partial Routines, `amount` stores the actual amount performed. The applicable target for the day or period may be fixed or may be calculated from the incremental Routine definition.

When `amount` reaches or exceeds the target, the RoutineCompletion automatically becomes `Done`. `amount` is not capped at the target; for example, `10 / 8` is valid.

If the User explicitly records `Won't_Do`, that state remains in the RoutineCompletion and breaks the streak.

### Period-based target

For Weekly, Monthly, or Yearly targets, each day retains its own independent RoutineCompletion, and progress for the period is calculated from the sum of the amounts recorded on days within that period.

Example:

```text
Routine: 100 km per month

Day 1 -> 5 km
Day 2 -> 8 km
...
Monthly progress = sum(amounts in month)
```

### Scheduling vs recorded reality

`start_date` and `end_date` define the interval in which the Routine is scheduled and presented as expected in the daily experience. This validity window does not prohibit recording reality outside that interval.

The User may:

- set a start date in the past;
- manually fill past days;
- record a completion on an unscheduled day;
- record a completion on a date before `start_date` or after `end_date`;
- edit or reset past completions.

After `end_date`, the Routine is no longer scheduled as an expected Routine for that day, but its history and the ability to record or correct completions remain available. The statistical effect of any historical edit follows the finalized statistical-window rules.

### Incremental target

For an incremental Routine, only `Done` completions increase the next target. A `Done` completion on an unscheduled day is also a qualifying completion.

After prolonged inactivity, the target gradually decays and may decrease back to the original baseline. The exact inactivity threshold and decay curve belong to the relevant specification/tuning artifact.

### Streak

Fixed-day Routines and frequency-based Routines have different streak semantics.

For a fixed-day Routine, a missed scheduled occurrence breaks the streak, and a completion on an unscheduled day does not repair a previously missed scheduled occurrence.

For `N times per period`, every valid `Done` increases the streak by one unit. An empty day inside the period does not by itself break the streak. At the end of the period, if the quota has not been completed, the streak becomes zero at the start of the next period; otherwise, the accumulated streak continues.

---

## 6.7 Recurrence

Recurrence may be defined using either the `Jalali` or `Gregorian` calendar. All day/month/year calculations must be performed in the selected calendar.

Task and Event may support recurrence at minute, hour, day, week, month, and year granularities, as well as supported advanced expressions. Routine supports only day-oriented recurrence at day/week/month/year granularities.

A Recurrence may use one of the following end conditions:

- no end;
- until a specific date;
- until a specified number of occurrences.

### Editing an occurrence

Edit behavior depends on recurrence semantics.

For calendar-anchored recurrence, such as recurrence on specified weekdays, changing one occurrence alone must not change the pattern of other occurrences. For example, if a Monday occurrence is moved to Tuesday, Saturday and Wednesday occurrences and occurrences in later weeks remain on the original schedule.

For interval/chained recurrence, such as **every three days**, when one occurrence is moved the User must be able to choose between:

- changing only this occurrence, allowing its interval from the next occurrence to differ temporarily;
- preserving the interval and shifting future occurrences accordingly.

Therefore, an occurrence may have an independent override without necessarily changing the Recurrence Rule of the entire series.

### Deleting an occurrence

When deleting a recurring occurrence, the User must be able to choose at least between:

- deleting only this occurrence;
- ending recurrence for future occurrences.

### Historical stability

Past occurrences are not rewritten by edits to the Recurrence Rule. Changes to the rule, calendar, or schedule apply from the change point forward and preserve prior history.

A recurring Event also generates its occurrences according to time; creation of the next occurrence does not depend on the previous occurrence finishing.

All-day recurrence uses the same calendar/date semantics and does not require a time of day.

The exact series/occurrence representation and persistence model are Design decisions.

---

## 6.8 Reminders

A Reminder exists only when the User sets it or when an AI-proposed Reminder is accepted by the User during Review. If no Reminder is recorded, the system must not send an implicit Reminder.

### Task and Event

The User selects a Reminder. If the Item has a reference time, the Reminder may be configured for that exact time or for one of a set of offsets before that time.

An Event Reminder is calculated relative to the Event's start time. A Task Reminder may be calculated relative to the Task's scheduled time.

Because relative Reminders are derived from Item schedule, changing the schedule must automatically update the trigger times of those Reminders.

### Routine

Routine Reminders are defined manually for specific clock times.

For a fixed-day Routine, the Reminder runs on valid scheduled days.

For a frequency-based Routine such as `3 times per week`, Reminders may continue on remaining days of the period until the quota for that period has been completed. After the quota is completed, remaining Reminders for the same period do not need to be delivered.

### Snooze and persistent alarm

The User may Snooze a Reminder.

At the domain level, a Reminder may carry a persistent/alarm-like intent. In the Current-Scope PWA, this intent must be implemented to the extent actually supported by the browser/OS and may be incomplete, degraded, or unavailable on some platforms. Lack of full native alarm integration in this phase must not remove or alter the intent stored in the domain.

When a native application is built for each OS in Future Scope, persistent/alarm-like behavior may be implemented more completely using platform-specific APIs, including capabilities such as a full-screen alarm, persistent ringing, and an explicit acknowledge/stop interaction. At that stage, options such as ringing indefinitely until acknowledgment or using a default ringing duration may be exposed according to actual platform capability.

### Completion and multi-device delivery

If an Item reaches a final outcome before a Reminder triggers, future Reminders for that Item no longer need to be delivered.

If the User has multiple devices, a Notification may be delivered to those devices until the User interacts with it on one device. After that interaction is recorded, the system must not continue delivering the same Reminder as a new Notification to the other devices.

---

## 6.9 Goals & Tags

Goal is an independent, AI-managed entity. The User does not create Goals manually and does not manually change the title of a system-generated Goal.

The User may edit a Goal's description. That description may provide additional context for future semantic analysis.

A Goal is not manually Archived or Reactivated. Its lifecycle is managed by the defined Goal Discovery and semantic-review behavior.

Every Goal belongs to exactly one List or Column context. At any given time, an Item is associated with at most one active Goal for Daily Ring attribution.

### Tags

A User-created Tag may be renamed or deleted by the User.

An AI-created Tag is not individually renamed, deleted, or archived by the User. The lifecycle of AI Tags is controlled by the AI Goal/Tag process.

The User may disable the entire Goal-discovery/intelligent-goal process. In that state, AI Tags generated by that process are removed and capabilities dependent on Goal/Daily Ring are disabled; core Task/Event/Routine management remains available. Disabling the global external-AI-processing control also disables this process and applies the same feature-level semantics to dependent capabilities.

The User cannot remove an individual AI Goal or AI Tag from AI management or permanently lock it against AI management.

---

## 6.10 Daily Rings

A Daily Ring is the daily representation of a Goal, but it is not merely a fixed collection of Items related to that Goal. Every Ring must be an **achievable plan for producing meaningful progress on that Goal within one Dotick Day**.

The number of Rings for a day follows this rule:

```text
eligible goals >= 3 -> exactly 3 rings
eligible goals = 2  -> 2 rings
eligible goals = 1  -> 1 ring
eligible goals = 0  -> 0 rings
```

The system selects the day's Goals. The User does not manually replace or reorder those Goals.

### 6.10.1 Daily plan structure

The conceptual Daily Ring model is:

```text
Goal
↓
Daily Ring
↓
Ring Group
↓
Daily Action
↓
Original Item
```

A `Daily Action` is not necessarily an independent Item in the system. It is part of the plan/snapshot for the specific Dotick Day and defines exactly what measurable amount or portion of the Original Item the User should perform today to make progress on the Goal.

If the Original Item can reasonably be completed in full on the same day, the Daily Action may represent completion of the entire Item.

If the Item is inherently larger than one day, the system must define a meaningful, measurable, and achievable portion for that day. Completing that Daily Action contributes to Ring progress, but it must not mark the Original Item itself as fully `Done` unless the Original Item's complete requirement has actually been satisfied.

Example:

```text
Original Task: Read book X completely
Daily Action: Read 10 pages of book X
```

Completing the Daily Action satisfies only the action for that day. The original Task remains open until its full requirement is actually completed.

### 6.10.2 Ring Groups

Daily Actions may be organized into one or more `RingGroup`s. Each RingGroup has a specific rule that determines the participation required from that Group for Ring completion.

Group rules may include behavior such as:

- completing all members of the Group;
- completing at least a specified number of members;
- earning at least a specified amount of score/credit from members;
- completing at least one option among multiple alternatives;
- limiting the maximum amount of credit obtainable from the Group.

Each Group may contribute a defined share of the Ring's total progress.

Some Groups may be a `hard requirement`. In that case, even if the User earns sufficient score from other Groups, the Ring does not become `Complete` until the hard requirement is satisfied.

Accordingly, a Daily Ring may represent a combination of mandatory, optional, and substitutable activities. Ring completion does not necessarily require completing every Item in a single linear list.

### 6.10.3 Feasibility and action generation

To build the day's plan, the system evaluates Items related to the Goal and determines how feasible each Item is for the same Dotick Day.

This evaluation must consider both the feasibility of the Item itself and the User's overall capacity for that day. Usable signals may include:

- relevance to Goal;
- urgency;
- importance/priority;
- deadline/timing;
- requiredness;
- estimated effort;
- difficulty;
- divisibility;
- substitutability;
- recent User capacity.

Difficulty/effort is a numeric signal that AI may estimate using authorized context. AI may also decompose a large Item into a meaningful Daily Action.

At this stage, AI produces analysis/proposals, but the final rules for progress, RingGroup satisfaction, and Ring completion must remain deterministic and reconstructable.

### 6.10.4 Initial generation and current-day replan

The initial Ring plan is generated at the start of the Dotick Day, and sufficient state for that day must be snapshotted so that the system can later reconstruct the decision that was made.

During the same Dotick Day, the current Ring may be replanned in response to meaningful changes. This does not conflict with historical snapshot semantics; the historical snapshot becomes fixed only after the Dotick Day is finalized.

An Item created during the day may pass through the relevance/feasibility pipeline. If it is appropriate for one of the day's active Rings, it may become a Daily Action and be added to the appropriate RingGroup.

Such a change must not rerun the day's Goal selection from scratch and must not make a Ring that has already become Complete incomplete again.

A change that makes the day's commitment meaningfully harder must be treated as a controlled `replan`, rather than merely inserting the Item into the existing plan without rebalancing it.

If the Original Item associated with a Daily Action is deleted during the same day, the corresponding Action must also be removed from the current Ring, and the plan must be replanned when necessary.

If User changes cause a Goal to have no valid remaining work during the same day, the Ring behavior depends on why the work disappeared:

- if no work remains because the User actually completed that work during the day, the Ring must preserve the day's context and the accomplished result;
- if no work remains because data was deleted or structurally changed, the current Ring may be replanned or replaced.

Semantic refresh operations that may change Goal/Tag relationships should, as far as practical, be ordered in the daily lifecycle so that they occur before generation of new Rings and do not unnecessarily destabilize the current plan.

### 6.10.5 Historical behavior

After finalization, the Daily Ring and its plan are historical snapshots. Future changes to the title, Tag, Priority, relation, or other fields of an Original Item must not rewrite the finalized plan for that day.

The historical snapshot must preserve at least the relationships among RingGroup, DailyAction, and Original Item, together with enough information to reconstruct the completion logic that applied on that day.

### 6.10.6 Progress, completion and challenge

`progress_percent` remains between 0 and 100 in the UI. Ring completion is determined by the deterministic RingGroup rules and hard requirements.

After the Ring reaches completion, the User may continue performing additional related activity. Such overachievement must not increase progress above 100 and may instead be reflected in `final_score`.

The User does not directly set the day's target or difficulty. The system must adapt challenge based on the User's actual behavior so that, with a reasonable amount of effort, completing at least one of the day's Goals and preserving the Global Streak remains realistic. If the User repeatedly cannot keep pace with the current challenge level, the system may gradually reduce difficulty/target.

At the same time, the upper achievement ceiling may remain challenging, and making the system easier must not distort actual progress.

### 6.10.7 Global streak when no Ring exists

If a Dotick Day has no eligible Goal and therefore no Ring is generated, the Global Streak neither increases nor resets; its value remains unchanged until a Ring becomes available for evaluation again. The same pause applies when a Ring cannot be created solely because a required AI/system dependency is unavailable and the User therefore had no valid opportunity for streak evaluation.

---

## 6.11 Dotick Day

Dotick Day is the system's logical day and is not necessarily the same as a Calendar Day.

The User may configure their day boundary. Changing the boundary must not redefine the current Dotick Day. The new setting takes effect starting with the next Dotick Day so that a User cannot manipulate the current day's result or historical attribution by changing the boundary.

Once created, each Dotick Day represents a real time interval whose boundaries can be converted to instants. A timezone change must not move the already-established instants of the current or past Dotick Days. The new timezone affects local presentation and future boundaries.

If the User has not configured an explicit boundary, the default ambiguity window is one hour after local midnight. A completion recorded during this window may be attributed to Today or Yesterday according to the User's explicit choice.

At the boundary, the conceptual lifecycle executes in this order:

1. the previous Dotick Day is closed;
2. the day's Rings and completion state are finalized;
3. final score/bonus is finalized;
4. related streaks are finalized;
5. the new Dotick Day's Rings are then generated.

If this lifecycle cannot execute exactly at the boundary instant, the system must be able to execute it later in a recoverable and idempotent manner without changing the day's actual effective boundary.

After finalization, the day's statistical outcome is closed. The Items themselves remain editable, but later edits must not rewrite the finalized statistical outcome of that Dotick Day.

---

## 6.12 Statistics & History

Dotick may present statistics, or use them for adaptive behavior, across windows such as Today, Week, Month, Year, Recent Behavior, and Lifetime.

Source data and report/finalized statistics are separate concepts. The User may later edit an old Item, but closing a statistical window fixes the outcome of that window.

While a window remains open, changing valid source data within that window may also change the statistics of that window.

After a window is closed:

- the report for that period is no longer rewritten;
- an annual report remains fixed after the year ends;
- a finalized Daily Ring is not reopened;
- changing a historical Item changes only the Item's current state/history and does not alter the recorded statistical outcome of the closed period.

Long-term aggregates must rely on finalized outcomes so that the contribution of a closed period does not silently change as a result of later Item edits.

### History and restore

The system must preserve sufficient history of persistent-domain changes for the User to inspect previous state versions and, in supported flows, restore or checkout those versions. The behavioral History model resembles a commit graph: if the User begins making changes from a historical version, a new branch is created from that point, and the previous path is neither deleted nor overwritten. The User must be able to inspect meaningful branches and versions and navigate/checkout among them.

After deletion, the UI must also provide a quick Undo mechanism so that an accidental deletion can be immediately reversed.

### Trash and permanent deletion

A deleted Item enters Trash. Trash is not permanent storage; after 30 days, an Item may be permanently removed from primary operational persistence.

Until permanent deletion occurs, the User may restore the Item.

After permanent deletion, the Item itself and its primary state are removed from operational persistence, but the history/audit necessary to record that the change occurred remains preserved.

---

## 6.13 Authentication

Using Dotick requires a registered Account.

Email/password authentication must include email verification, and the User must be able to reset their password through email.

Every User has a unique username/handle, a display name, and an optional `Profile Picture`. A username may be changed, but uniqueness must remain enforced. A display name does not need to be unique. The Profile Picture is part of the Account's identity presentation and does not create a Public Profile or an independent social-network capability.

An email address or phone number may be added to the Account and used as a contact/discovery identifier only after ownership has been verified using the appropriate verification code. When an email address or phone number is added, Dotick must send a verification code and must not register that value as an active Account contact until verification succeeds. Therefore, an unverified identifier cannot be used for discovery or for flows that depend on a verified contact.

Dotick may connect multiple authentication methods to one Account so that different login methods resolve to the same User identity. Within Current Scope, Google is the only external identity provider; email/password and Passkey are independent Dotick authentication methods. Exact account-linking behavior is defined in Authentication Design.

Passkey is an optional authentication method. An Account that uses Google is not required to add a password or Passkey in order to continue using the Account, but the system must offer and recommend adding an independent fallback.

The User must be able to view active sessions and revoke a specific session. The User must also be able to log out all devices.

Authentication-provider failure must not unnecessarily make existing data in a valid Offline session unusable. Initial authentication and operations requiring the server still require valid connectivity.

---

## 6.14 Groups & Sharing

Collaboration in Dotick is based on two independent but complementary concepts:

```text
Resource Sharing
= granting controlled access to a specific Resource

Group Collaboration
= creating a persistent context for multi-user collaboration
```

`Group` is not the universal or mandatory mechanism for Sharing. A User may Share a specific Resource with another User or with a Group. A Group is used when collaboration requires membership, roles, shared ownership/context, and multi-user workflow.

### 6.14.1 Shareable Resource Scope

Within Current Scope, Sharing may be applied at the following Resource scopes:

```text
Folder
List
Item
├── Task
├── Event
└── Routine
```

Sharing by itself does not change Resource ownership. A Resource must retain the identity of its owner or ownership scope, and the UI must be able to show which User or Group owns the Resource.

Shared access must be revocable and remains independent from the lifecycle of Group membership unless the source of that access is itself GroupMembership.

### 6.14.2 Authorization Model

Authorization must be evaluated based on the capabilities granted to the actor for the Resource, not merely based on Role names.

```text
Direct Sharing
└── Access Profile

Group Collaboration
└── System-defined Role
```

Access Profiles and System-defined Roles are separate concepts. Current-Scope Access Profiles may include `Viewer`, `Commenter`, `Contributor`, and `Manager`.

Collaboration capabilities may include view, comment, edit, move, claim, assign, manage_structure, manage_members, manage_sharing, and other permitted interactions.

Custom Roles and arbitrary permission composition do not exist in Current Scope.

### 6.14.3 Field Visibility

Access to an Item does not necessarily imply visibility of all of its user-facing information. The Owner or another authorized actor may restrict visibility at the level of product/domain field groups.

These groups may include Basic Information, Schedule, Status/Progress, Description, Location, Attachment, Tag, Completion History, Recorded Amount, Note, and Statistics.

Internal sync, audit, authorization, versioning, or storage metadata is not shareable merely because it exists in persistence.

### 6.14.4 Container Sharing and Inherited Access

Sharing a container may be inherited by its descendants:

```text
Folder
└── List
    └── Item
```

The inheritance model in Current Scope is intentionally simple and does not currently require complex per-descendant explicit-deny exceptions.

Before actions that Share or revoke a significant number of Resources through inherited access, the system must show the initiating User the scope of the effect and obtain explicit confirmation.

### 6.14.5 Group-owned and Group-scoped Resources

A Folder, and content created directly within a Group context, is owned by that Group and does not disappear when its creator leaves the Group.

A personal Resource may also be placed into a Group context. In that case, the prior owner's identity must be preserved, but while the Resource remains within the Group context it follows that Group's authorization and collaboration rules. Only the prior owner may remove their personal Resource from the Group context.

A Group-owned Resource is not visible to a User without valid access to the Group. A Group-owned Resource must not bypass Group authorization by being Directly Shared with an actor outside the Group.

### 6.14.6 Group Collaboration

A User may belong to multiple Groups, and every GroupMembership within Current Scope has a System-defined Role.

A Group may collaborate on shared Resources. Members may perform only those operations allowed by their effective permissions.

Membership alone does not create unrestricted access to every Resource in the Group. Final authorization remains valid at Resource scope.

### 6.14.7 Assignment and Responsibility

Assignment and Authorization are independent:

```text
Authorization = what operations is the actor allowed to perform on the Resource?
Assignment    = which User or Users are responsible for performing the Task?
```

A Task may be assigned to multiple Users who already have the necessary access. Claiming a Task likewise does not create access; it changes responsibility only.

### 6.14.8 Collaboration Interactions

Comments must follow the authorization rules of the corresponding Resource.

Lightweight interactions such as `Nudge` may be separate permission-controlled capabilities and do not have to be modeled as Comments.

Notifications and realtime updates must not disclose information beyond the recipient's effective access.

### 6.14.9 Access Change and Revocation

Any change that removes an actor's access path must be reflected in effective authorization. If server-side access has been revoked, a new operation by that actor must not be considered valid merely because the actor previously possessed a local copy.

Revoking access must not change Resource ownership or remove required audit/history.

### 6.14.10 Group deletion

Deleting a Group is a broad destructive operation. Before deletion, the Manager must be warned that Resources owned by or dependent on that Group will also enter the deletion flow and should be transferred beforehand when necessary.

If the Manager confirms deletion, Resources are not automatically transferred to another User; they enter Trash.

The Manager who deleted the Group must be able to restore the Group and its Resources during the Trash retention window. The current Trash retention window is 30 days.

---

## 6.15 Offline & Sync

Dotick's core productivity flows must remain usable without an Internet connection.

At minimum, Offline behavior includes:

- creating/editing/managing Tasks;
- creating/editing/managing Events;
- creating/editing/managing Routines and RoutineCompletions;
- creating and managing Folder/List/Column;
- moving Items among containers;
- creating Comments on a Resource for which valid local access had previously been established.

Group membership management, Sharing, invitations, and other operations that inherently require current server-side authorization or membership state are online-only.

A User who has previously authenticated successfully must be able to open and use the application Offline within the scope of their local replica.

### Local replica scope

A device is not required to keep the User's entire unlimited history Offline at all times. The current working set and data necessary for core Offline flows must be local. Very old historical data may be fetched from the server on demand when connectivity is available.

### Attachment cache

Attachment binaries are part of the local-replica model, but every file visible to the User does not need to be permanently downloaded to every device. Attachment metadata and relations must remain representable in the working set even when the corresponding binary is not present on that device.

A file uploaded or selected from a device must remain openable without being downloaded again as long as a local copy still exists on that device. On another device, the binary is downloaded when needed unless that device's policy selects it for automatic download.

Each device must maintain an independent local Attachment cache and the User must be able to control its policy. Product-level controls must include at least:

- which Attachments are downloaded automatically;
- how long cached binaries are retained, including an indefinite-retention option;
- the overall cache-size limit on that device;
- a device-wide default with overrides for a specific Folder or List.

When multiple policies apply, the policy closest to the Resource takes precedence for that Resource's cache behavior; for example, a List policy overrides its Folder policy, and a Folder policy overrides the device-wide default. Exact policy categories, eviction ordering, and storage bookkeeping belong to Offline/Storage Design.

When retention or cache-size policy allows eviction, Dotick may remove eligible local binaries from the device to free space. This eviction changes only the local cache and must not delete the server-side Attachment, its metadata, or its relation to the Item. When connectivity is available, an evicted file must remain downloadable again. An Attachment using `Keep indefinitely` or an equivalent policy must not be removed by ordinary cache cleanup unless the User changes the policy or explicitly removes the local copy.

If the binary is not present on the device and connectivity is unavailable, that Attachment may temporarily be unavailable for opening. This must not make the Task/Event/Description or the Resource's other local data unusable.

### Reconciliation

Offline changes are retained locally. After reconnection, the device sends those changes to the server; the server reconciles them with existing state, reaches a converged state, and makes that result available for synchronization to other devices.

The conflict baseline is field-level, and ordinary conflict resolution should be automatic as far as reasonably possible.

If two actors/devices change the same field and conflict resolution causes one value to replace another, history must show which actor recorded which value and how subsequent state reached the current value.

### Revoked access while offline

If a User edits a Shared Resource while Offline but their access is revoked on the server before synchronization occurs, the edit must not be applied to the Resource after reconnection, even if the local edit timestamp precedes the revocation time. Current server authorization at operation acceptance time is authoritative.

This rejection must not silently destroy the local change; history/recovery must preserve enough information to understand the outcome.

### User sync interaction

The User may request an immediate sync/update through an ordinary client refresh interaction such as pull-to-refresh. Transport details and background-sync scheduling belong to Design.

All online devices must converge to the server's converged state, and an Offline device must reconcile to the same state when it reconnects.

---

## 6.16 AI-assisted Item Creation

Within Current Scope, AI-assisted creation is a **Voice-based** pipeline for creating `Task`, `Event`, and `Routine`. User-typed text is not an input to AI-assisted creation; if the User wants to enter text, they use ordinary manual creation.

One input may produce one or more Item proposals. When multiple Items are proposed, the User must be able to review, edit, accept, or reject each proposal independently.

Conceptual pipeline:

```text
Voice
    ↓
Speech-to-Text / Normalization
    ↓
Intent + Entity Analysis
    ↓
One or More AI Item Proposals
    ↓
Review
    ↓
User Edit
    ↓
Confirm
    ↓
Create Real Item(s)
```

Before Confirm, proposals are not real Items.

When sufficient evidence exists, AI may infer or propose:

- Item type: Task / Event / Routine;
- title;
- date/time;
- recurrence;
- location;
- description;
- Folder/List/Column;
- Reminder;
- Priority;
- Deadline and Grace Period;
- Tag;
- other valid inferable fields.

AI must not create or propose dependency relationships or structural parent/child relationships on the User's behalf.

For example, an input such as **“Weekly meeting with Ali, Wednesday at 8 PM”** may produce a weekly recurring Event proposal even if the User did not explicitly use the technical term recurrence.

### Context

AI may use relevant context only within the actor's effective authorization and field visibility. Valid permission to view data, including Shared data, is sufficient for that data to be used as AI context. AI must not send to the provider any field or Resource the actor is not authorized to view. Permitted context may include:

- the User's current input;
- existing Folder/List/Column structures;
- Tags;
- User Preferences;
- previous Items and recent behavior;
- any other context explicitly permitted by that capability.

AI must not bypass authorization. Before actual creation, every proposed destination and field must pass the same validation and permission rules that apply to manual creation.

### Review and provenance

During Review, the User may change the Item type and any proposed field.

The Review UI must be able to show field provenance, for example whether a field came from explicit input, was AI-inferred, or was inferred from a User preference.

Before Confirm, the final proposal must be validated against ordinary domain rules. Prompt/output schema should also guide the model toward producing a valid payload as much as possible, but application validation remains independent from model output.

If the User Cancels or Rejects a proposal/session, that draft session is not retained within Current Scope.

### Microphone dependency and failure behavior

Starting AI-assisted creation depends on microphone capability and the required client permission. If Dotick does not have microphone access, Voice AI creation must not execute, and the User must see a clear message that microphone access is required and the corresponding permission must be granted. Current Scope does not provide a typed-text AI fallback for this case; ordinary manual creation remains available.

If the AI provider or Speech-to-Text capability is unavailable, only that AI-assisted flow must show an appropriate error. Manual Item creation and other core capabilities independent from AI must remain usable. From the System Definition perspective, Speech-to-Text may be local, platform-provided, or external; the implementation choice must not change the semantics of this flow.

---

# 7. Domain & Business Rules

> This section records rules that are not merely descriptions of a single feature and must hold throughout the system. These rules express business/domain meaning, not the storage or code mechanism used to enforce them.

## 7.1 Ownership, Scope & Identity

Creator identity, ownership, and the current context of a Resource are independent concepts and must not be used interchangeably.

`created_by` must historically preserve the identity of the User who originally created the Resource. Transferring the Resource, changing ownership, placing it into a Group context, or changing permissions must not rewrite `created_by`.

Being the Creator does not by itself grant any special permission. If a User who created a Resource later loses valid access to that Resource, Creator status alone must not preserve the ability to view or modify it.

A personal Resource may be placed into a Group context without necessarily transferring personal ownership to the Group. In that case:

- the Resource retains its previous personal owner;
- while it remains in the Group context, its collaboration operations follow that Group's authorization rules;
- only that personal owner may remove the Resource from the Group context, unless a future explicit ownership-transfer behavior is defined.

By contrast, a Resource created directly within a Group context is Group-owned. The human Creator of that Resource does not acquire personal ownership merely because they created it, and the Creator leaving the Group must not change Resource ownership.

Resource ownership does not have to match container ownership. For example, a personal Task or Event may be placed in a container owned by a Group or by another User, provided that placement and authorization are valid. Placement in a container alone does not transfer ownership of the Resource.

`Source` also remains independent from ownership and Creator identity and expresses provenance only.

---

## 7.2 Recorded Reality, Authoritative State & Finalization

Dotick must distinguish between **what was planned** and **what was actually recorded**. Domain source state must preserve the reality recorded by the User even when that reality does not match the prior schedule.

Therefore, schedule, recurrence, validity window, and other planning rules may determine eligibility, presentation, Reminders, streaks, scoring, or other consequences, but by themselves they must not prevent a valid fact from being recorded. Examples include editing a historical Item and recording a RoutineCompletion on an unscheduled day or even outside the Routine's defined validity window.

Derived data such as Statistics, streaks, Daily Ring progress, recommendations, and aggregates must not replace operational source data as the source of truth. While a derived state remains open and recomputable, it must be re-derived from valid source state when the two are inconsistent.

### Finalized historical artifacts

A derived artifact that has been explicitly `finalized` according to a business rule is no longer merely a temporary cache; it becomes the historical business record for that interval.

After finalization:

- later changes to historical Items remain allowed;
- operational history and state may continue to change;
- however, the recorded outcome of a closed statistical window must not be rewritten;
- a finalized Daily Ring and its final snapshot must likewise not be recalculated or rewritten because of later edits to source data.

Within an interval that has not yet been finalized, valid source-data changes may change the derived result for that interval.

Therefore, immutability applies to the **finalized artifact**, not to the Item or operational data that happened to be created in the past.

---

## 7.3 Structural Placement, References & Access Boundaries

Task and Event use the main organization hierarchy. At any given time, each belongs to exactly one List and exactly one Column within that List.

Routine does not follow this placement rule. A Routine is not placed in Folder/List/Column and has its own dedicated product space.

### Structural placement

A structural Parent and child of type Task/Event must have compatible organizational placement. While the structural relation exists, the Parent and all structural descendants are placed in the same List and Column.

Moving the Parent to another location moves its structural descendants together with it. If the User independently moves a child to another incompatible placement, the structural relation between that child and Parent is broken, and both Resources retain their independent identities.

Cycle prohibition is not a universal invariant for every relationship in the system. Each relationship has validation based on its own semantics. Within Current Scope, both the structural parent/child hierarchy and the Task dependency relation prohibit cycles, but this rule must not be generalized automatically to every future relation type.

### References

A Reference is independent from structural placement. A Task, Event, or Routine may be referenced from another context provided that the viewer currently has valid access to the referenced Resource. A Reference does not transfer ownership, placement, or structural parenthood.

As long as access remains valid, the Reference representation must show the current state of the referenced Resource.

If the viewer later loses access to the referenced Resource, the Reference must not expose subsequent updates to that Resource. In that state:

- the last title and state that the viewer was validly allowed to see before revocation may remain visible in the Reference;
- the Reference must clearly indicate that the Resource is no longer accessible;
- no new change after access revocation may be transmitted to the viewer through the Reference.

This behavior is distinct from deletion of the Resource; deletion of a referenced Item follows its own deletion/history rules.

---

## 7.4 Cascading Operations & Atomicity

Some operations have consequences for structural descendants because of the semantics of the Resource itself. These consequences are part of the behavior of the initiating action and must not leave the system in a partially applied state.

### Delete cascade

Deleting a structural Parent also places all of its structural descendants into the same deletion flow.

If the actor has valid permission to delete the Parent, that same permission is sufficient to execute the **intrinsic delete cascade** on structural descendants; separate delete permission does not need to be re-established for every descendant.

Before executing a destructive cascade that affects multiple Resources, the system must show the scope of the effect to the User in an understandable form and obtain explicit confirmation.

### Completion cascade

If Task rules specify that marking a Parent `Done` also marks structural descendants `Done`, valid permission to perform the action on the Parent is sufficient for that intrinsic completion cascade as well.

This rule covers only the consequence defined for that specific action. It does not create general or permanent permission over the children.

If the optional `Won't_Do` cascade setting is enabled, that cascade follows the same action-level semantics.

### Move cascade

Move differs from delete/completion. Because moving a Parent also changes the independent placement of its descendants, permission on the Parent alone is not sufficient to move all descendants.

The actor must have the necessary permission for every Resource whose placement changes as a result of the operation. If this requirement is not satisfied for even one affected Resource, the operation must not be partially applied.

### Atomicity of multi-resource consequences

Any multi-Resource operation whose consequences must be applied as one unit to preserve consistency must either succeed completely or not be applied at all.

If authorization, validation, or a domain constraint prevents part of the consequence from executing, the entire operation is canceled and the system must not leave a partially changed structure.

This rule defines the business outcome of the operation. The transaction, locking, rollback, or other implementation mechanism belongs to Design/Data/API specifications.

---

# 8. System-wide Behaviors

> This section defines behaviors that are not limited to one capability and must have consistent semantics throughout Dotick. Implementation, storage, protocol, scheduling mechanism, and technical algorithm details are defined in the relevant Design artifacts.

## 8.1 Time & Timezone

Dotick must distinguish among an `absolute instant`, local time representation, and domain business dates.

Every Task or Event that has a schedule must resolve that schedule to one or more real, convertible instants. This requirement applies only once the Item is time-bearing; it does not require an unscheduled Event to have a start time or all-day date merely in order to exist. The rule applies equally to personal and Shared Resources; Sharing is not a prerequisite for this temporal rule.

### Account timezone

Each Account has an effective timezone that is used for local time presentation and for calculating the User's future boundaries.

On first use, the timezone may be automatically suggested or initialized from the device, but the User must be able to change it manually.

If the device timezone later changes, Dotick must not silently change the Account timezone without informing the User. The system must detect the device-timezone change and ask whether the User wants the Account timezone to change to the new timezone as well.

Timezone is an Account-level setting, and all of the User's clients must use the same effective Account timezone for product semantics. A device may have a different local timezone, but until the User confirms a change to the Account timezone, that device-level difference must not alter the Account's time semantics.

### Timed Items

Changing the Account timezone must not move the real instant of an existing Task or Event. Only the local representation of that instant changes in the new timezone.

For example, if an Event displayed at `20:00` in the original timezone refers to a particular instant, the same instant may later be displayed as `15:30` or `22:00` after the timezone changes. The system must not modify the Event's real time merely to preserve the previous local clock value.

A recurring timed Item must likewise keep its occurrences tied to real instants. Changing the Account timezone alone must not re-anchor the recurrence. The same occurrence is displayed at the corresponding clock time in the new timezone. If the User wants future recurrence to be based on the new local clock time, that is an explicit schedule edit, not an automatic consequence of changing timezone.

### All-day Items

All-day is not merely a presentation state with no clock time that can be re-anchored to the same local date after a timezone change. When an all-day Task/Event is defined, the selected Calendar Day must be converted to the real interval corresponding to that day in the effective timezone at that time.

After that interval is established, a timezone change must not move its start/end instants. In the new timezone, the same interval may no longer appear exactly as `00:00` through `23:59` of one local Calendar Day and may even span parts of two different Calendar Days.

The system must perform this conversion automatically and all clients must continue to refer to the same real interval.

### Business dates

Business dates such as `RoutineCompletion.occurrence_date`, or the attribution of a completion to a Dotick Day, are not necessarily the same as the Calendar Date of the timestamp at which the action occurred or was recorded. The system must keep the real occurrence/recording timestamp independent from the business date or credited day.

---

## 8.2 Dotick Day / Day Boundary

`Dotick Day` is a logical daily interval used for attribution, Daily Rings, streaks, and finalization and is not necessarily equal to a Calendar Day.

The User may configure the day boundary to any valid time of day. There is no fixed product-level rule restricting the boundary to midnight or to specific nighttime hours.

A boundary change does not apply to the current Dotick Day and becomes effective starting with the next Dotick Day. This prevents a User from shifting current-day attribution or outcomes after those results have already begun to form.

Once established, each Dotick Day must refer to a fixed real-time interval. A later timezone change must not change the start or end instants of the current or a historical Dotick Day; the new timezone is used only for presentation and for calculating future boundaries.

### Ambiguity window

If the User has not defined another explicit day boundary, completions recorded during the default one-hour ambiguity window after local midnight may be attributed to either `Today` or `Yesterday`.

This attribution is decided independently for each completion. Choosing the attribution of one completion must not automatically determine the attribution of another completion.

Until the User chooses the credited day for an ambiguous completion, that completion must not be included in Daily Ring, streak, or Today/Yesterday statistics calculations. The source action may remain recorded, but its day-based effect remains unresolved until attribution is determined.

### Boundary processing

At the boundary, conceptual behavior must execute in this order:

1. close the previous Dotick Day;
2. finalize the day's Rings and outcomes;
3. finalize the day's final score and bonuses;
4. finalize related streaks;
5. then begin new-day generation if the required dependencies are available.

If the device or server is unavailable at the exact boundary instant, finalization must later be performed in a recoverable and idempotent way, while the effective boundary remains the original instant.

While Offline, the client must be able to perform deterministic finalization of the previous day locally. If generation of the new Daily Ring requires online AI and AI is unavailable, finalization must not be blocked; only the new Ring remains ungenerated until valid AI access becomes available.

---

## 8.3 Audit & History

Dotick must preserve visible and recoverable history for meaningful changes to persistent domain state.

History must be able to retain at least the actor identity, affected Resource or entity, action type, change time, and enough information to understand the previous/current state or a meaningful diff. Merely viewing a Resource or performing a normal read is not part of this product-level History; access/security logging, if needed, is a separate concept.

An ordinary User must not be able to edit or delete an existing Audit/History entry.

### Branching history

Dotick History is not merely a linear timeline in which the past can be overwritten. The User must be able to inspect meaningful previous versions of a Resource and `checkout` a prior version.

If the User continues making changes from a historical version, the previous history must not be deleted or overwritten. Instead, a new branch is created from that point.

For example:

```text
V1 ── V2 ── V3 ── V4
      \
       └── V2' ── V3'
```

The User must be able to visually inspect the available paths and branches and, within supported capability, checkout another version or branch.

A checkout or restore creates a new history event and must not destroy previous branches.

This behavior does not require a particular implementation such as Git, full event sourcing, or a specific storage graph. The requirement is only for the externally observable semantics of branching, preservation, and navigation of history.

User-facing `History`, internal `Audit`, and metadata used by Offline/Sync must not become three independent and conflicting sources of truth. Design must build them on compatible identity/version/order semantics so that a change, restore, conflict, or branch is not interpreted inconsistently across these layers. The exact implementation may differ, but stable identity and traceable relationships among the layers must be preserved.

### Shared Resource history

Any actor with valid access to a Resource may view the history that is allowed to be presented for that Resource. History presentation must still not reveal information that the actor is not permitted to view under current authorization.

Finalized statistical artifacts and historical Daily Rings follow finalization rules. Checking out or editing a historical Item must not rewrite the finalized outcome of a closed period.

---

## 8.4 Soft Deletion

Ordinary deletion in Dotick must be recoverable for supported Resources and must not, by default, immediately convert state into permanent deletion.

The following Resources may enter Trash:

- Folder;
- List;
- Task;
- Event;
- Routine;
- Group;
- Comment;
- Tag.

`Column` is not managed as an independent Trash-managed Resource within Current Scope. `RoutineCompletion` also does not enter Trash; its reset/delete semantics follow the History rules of Routine/RoutineCompletion. Goal follows its own AI-managed lifecycle within Current Scope and is not defined as a general Trash-managed Resource.

After deletion, the UI must provide a quick Undo option.

### Retention and permanent deletion

The current Trash retention period is 30 days. If a Resource is not restored during this period, permanent deletion may occur automatically.

The User must also be able to explicitly choose `Delete Permanently` before the retention period expires.

Permanent deletion removes the Resource's operational state from primary persistence, while the history/audit required to record that the Resource existed and what changes occurred to it may remain preserved.

### Restore

If a container and its subtree were deleted together, restoring the entire container should, as far as possible, restore the previous structure and the related trashed descendants.

If a Task or Event is independently restored but its original List/Column no longer exists or cannot be restored, the Resource must be moved to the `Inbox` and its default Column so that restoration does not fail merely because the previous placement no longer exists.

Restore must not erase deletion history; both deletion and restoration must remain visible in History.

---

## 8.5 Offline Behavior

Offline-first behavior is a core Dotick principle. Every core capability whose semantics do not inherently require the server or current remote authorization should, as far as practical, execute on-device without waiting for the network, and its Offline experience should remain close to Online behavior in speed and usability.

This principle applies only while preserving full Offline behavior does not cause severe quality degradation, unreasonable storage/energy consumption, or an unavoidable dependency on an Online service.

### Offline-capable behavior

At minimum, the following behaviors must be executable Offline:

- create, view, and edit Task;
- create, view, and edit Event;
- create, view, and edit Routine and RoutineCompletion;
- create and manage Folder/List/Column;
- locally move and organize Resources;
- Comment on Resources for which valid local access was previously established;
- use and advance a Daily Ring that was already generated for that day;
- generate recurrence occurrences when the required rule and state exist on the device;
- execute a previously schedulable local Reminder or alarm within platform capability;
- deterministically finalize the previous Dotick Day.

Sharing, invitations, Group membership management, and operations that depend on authorization/current server state remain online-only.

### Local success and pending sync

If an operation is Offline-capable, loss of network connectivity or a temporary server failure must not force the User to wait for reconnection. The action must be applied to valid local state and retained as pending synchronization.

The User must be able to see the result of the local action immediately in the client. Later synchronization is responsible for reconciling it with the server.

A sync failure must not silently remove the local change. If the change is rejected or another value wins a conflict, history/recovery must be able to explain the outcome.

### Multi-day Offline operation

If the User remains Offline for multiple days, recurrence and deterministic core planning behavior must continue using local state.

An existing Daily Ring remains usable Offline. However, generation of a new Ring that requires AI is online-only. If AI or the network is unavailable at the beginning of a Dotick Day, the system does not create a fabricated or lower-quality fallback Ring; generation is postponed until AI becomes available again.

---

## 8.6 Conflict Behavior

The goal of conflict handling in Dotick is to reach a converged state automatically without silently losing meaningful information.

Ordinary conflict resolution should be automatic as far as practical, and the User should not be forced to manually choose a winner for routine conflicts.

### Field-level convergence

Changes to independent fields of a Resource may be merged. If multiple actors/devices change the same field, the change with the later valid ordering is the baseline winner for that field.

The exact timestamp, logical-clock, version-vector, or other ordering-metadata mechanism is defined in Sync Design; the System Definition specifies only the required behavior.

Concurrent movement of the same Resource to different locations is treated as a conflict on that Resource's placement, and the later valid change determines final placement.

### Delete and later edit

Delete does not absolutely and permanently override every later edit. Valid operation ordering determines final semantics.

If a Resource is deleted first and a valid later-ordered edit exists for the same Resource, the behavior is equivalent to:

```text
Delete
↓
Trash
↓
Restore
↓
Apply later Edit
```

Accordingly, the later edit may restore the Resource from Trash and apply the edit.

If the edit occurs before the delete and the delete operation is ordered later, the Resource remains in Trash.

This behavior is different from revoked authorization. If the server has revoked the actor's access, that actor's Offline edit is not accepted after reconnect even if its local timestamp is before or after the revocation; current server authorization is a prerequisite for accepting the operation.

### Conflict visibility

Resolved conflicts do not need to generate a separate Notification or banner. History must allow an authorized actor to see what changes occurred, which value replaced another, and the sequence from which the current state resulted.

---

## 8.7 Notifications

Notification behavior in Dotick is cross-device and permission-aware and must distinguish between Item-level Reminders and workflow/collaboration Notifications.

### Category controls

The User must be able to independently configure or disable the primary Notification categories, for example:

- Item Reminders / Alarms;
- Comments / Mentions;
- Group / Sharing / Invitations;
- Nudge and collaboration interactions;
- Gamification / motivational notifications.

These category settings must not change the permissions or underlying domain state of the associated action; they control only Notification delivery/presentation.

### In-app Notification Center

Dotick must provide an in-app Notification Center for Notifications that are part of application workflow or in-app messaging, such as invitations, membership/share requests, actions the User must accept/reject/review, and product/system updates that are app-level in nature.

Ordinary Item Reminders and alarms must not be stored and displayed in this Notification Center merely to create an additional inbox or history. The Reminder remains valid in the domain, while its presentation occurs through the platform's notification/alarm capability.

### Delivery permission

Not granting, or later revoking, browser/OS Notification permission must not disable the corresponding Reminder/Notification capability or domain state. Dotick must preserve the required scheduling and internal state, but if the platform does not permit Notification display at delivery time, the message is not shown to the User outside the application. This failure must not cause missed Reminders to accumulate in the in-app Notification Center.

The client must be able to show Notification-permission status to the User and, where the platform permits, provide the flow for requesting permission. All other Dotick capabilities must remain usable without Notification permission.

### Cross-device interaction

Interaction state for a Notification must be synchronized across the User's devices.

If the User completes a final interaction with a Notification, the same Notification must not later be sent as a new Notification on another device. A device that was Offline at the scheduled time must likewise not deliver the original Notification after reconnect if that Notification has already been handled on another device.

This rule applies to all Dotick Notifications, not only Reminders.

`Snooze`, or actions such as **remind me again in 15 minutes**, are not final interactions. Such an action creates a new trigger, and the subsequent Notification must be deliverable at the new time to all eligible devices.

---

## 8.8 Error & Failure Behavior

Failure in Dotick must not cause silent data loss, false success, or partially applied state.

### Offline-capable operations

An operation defined by the System Definition as Offline-capable must continue locally even during network/server failure. The User must not have to wait for connectivity in order to create/edit/manage core data.

In this state, the client may report valid local success and retain the operation as pending future synchronization.

### Validation failure

If an action is rejected because of validation or a domain rule:

- the previously valid state must not be corrupted;
- the User must see an understandable reason for the failure;
- entered input should be preserved as far as practical so the User can correct it;
- invalid state must not be inserted into the domain merely to avoid presenting an error.

### Online-only operations

Operations such as Share, Invite, or Group membership changes that depend on the server/current authorization must not report local success when their result is not confirmed.

If network interruption makes the result uncertain, the client must re-verify authoritative state from the server and must not show definitive success until that state is confirmed.

### Multi-resource operations

Operations that must be atomic according to domain rules either apply completely or do not apply at all. Failure in one part of a cascade or validation must not leave partially applied state.

Error presentation must be product-level and understandable. Raw technical details from a provider, database, or stack do not need to be shown directly to the User.

---

## 8.9 AI Failure Behavior

AI failure must remain isolated to the capability that depends on AI and must not make core Task/Event/Routine management, Offline data entry, or other AI-independent behavior unavailable.

AI output may affect domain state only after Dotick validation. A malformed, incomplete, or invalid response must not be treated as valid merely because it was returned by a provider.

### Partial proposal failure

In AI-assisted Item Creation, proposals are independent review units. If one input produces multiple proposals and only some are valid, the valid proposals must still be shown to the User while invalid proposals fail independently.

Failure of one proposal must not invalidate the healthy remainder of the batch.

### Goal/Tag processing failure

If Goal Discovery, semantic review, or AI Tag processing fails, the previously valid Goal and AI Tag state must remain unchanged.

The system may retry the process later, but failure must not delete, archive, or modify a previous Goal or Tag unless a new valid result has actually been produced.

### Daily Ring generation failure

If a required AI dependency for Daily Ring generation is unavailable at the start of the Dotick Day, Dotick must not create an incomplete Ring or a simplified fallback that does not meet the expected quality/semantics and present it as a valid Ring.

In that case:

- the core application and AI-independent capabilities continue to work;
- the previous Dotick Day may still be finalized;
- no new Ring is generated until valid AI access is restored;
- once AI returns, generation may occur for the current Dotick Day if that generation is still valid under the lifecycle;
- the Global Streak is `paused` while no evaluable Ring exists solely because of this system/AI failure: it neither increases nor resets.

This pause is not equivalent to User failure. When a valid Ring was generated and the User had a real opportunity to complete it, the Global Streak follows the ordinary completion rules for that day.

Provider lists, retry policy, timeout, and routing strategy among service-managed providers are Design details and must not alter the semantics above. The fallback from a failed personal credential to service-managed AI, as defined in Section 9.2, is product behavior and may not be reversed by Design.

---

# 9. External Systems & Integrations

> This section defines only interactions and division of responsibilities. Exact protocol, payload, endpoint, and authentication contracts belong to Design/API specifications.

## 9.1 Authentication Provider(s)

Within Current Scope, `Google` is the only supported external authentication provider. Google is responsible for executing the external authentication flow and providing the identity assertion required to prove identity; Google is not the source of truth for Account state, authorization, or Dotick data.

After external authentication, Dotick maps the external identity to its own internal Account and remains the owner of application state such as username/handle, email/phone discovery state, sessions, authorization, GroupMembership, Sharing state, and product data.

Email/password and Passkey are authentication methods independent from Google. A User who signs in through Google is not required to configure another password or Passkey in order to use the Account, but Dotick must provide the ability to add an independent fallback and should recommend doing so as a way to reduce dependency on Google. Therefore, a Google outage may temporarily restrict new login for an Account without an independent fallback, but it must not unnecessarily make local data in a valid Offline session unusable.

Email verification and password reset are Dotick-owned business/security flows. Dotick controls the required token/state, validity, verification/reset result, and Account changes; if external email-delivery infrastructure is used, it is responsible only for transporting the message to the recipient. Vendor selection, protocol, template transport, and delivery details belong to Design.

## 9.2 AI Provider(s)

AI model inference occurs outside the System Boundary, but full orchestration belongs to Dotick. Dotick determines what context is permitted, how prompts/instructions are constructed, what structured output is expected, how responses are validated, and under which domain rules the result may affect product state.

By default, AI runs using credentials/providers managed by the Dotick service. In this mode, Dotick selects the provider and model; the User does not select the service-managed provider or model. Displaying the exact provider/model used is not a general product requirement.

The User may provide a personal credential/API for a supported provider and enable personal-credential mode. In this mode, compatible requests are first executed using the User's personal credential. The User must be able to return to the default service-managed mode at any time.

Validity of the personal credential, quota, billing, provider-account restrictions, and the terms of use of the personal provider are the User's responsibility. Dotick does not guarantee that the personal credential is always valid, has available quota, or is free of charge. Dotick's responsibility in this mode is limited to secure use of the credential within the supported flow and application of the product-defined fallback behavior.

If the personal credential is invalid or unusable when a request executes, Dotick may automatically continue the same request using its default AI service. After such a fallback, the system must visibly but non-blockingly indicate that the personal credential was not used and the Dotick service was used instead; a separate popup or confirmation is not required. If the service-managed path is also unavailable, failure follows the ordinary AI Failure Behavior rules.

Any data that the actor is authorized to view under effective authorization and field visibility, including Shared data, may be used as context for an authorized external-AI-processing capability. AI processing must not create new access and must not send any Resource or field to the provider that the actor is not permitted to view.

Before external AI processing is enabled or first used, the User must be clearly informed and must accept that their authorized context—which may include Shared data they are permitted to view under effective access—will be sent to third-party infrastructure/providers in order to perform the AI capability. Acceptance of this boundary is a prerequisite for using external AI processing, and the User may disable that processing using the global AI control. This acceptance must include acknowledgement of the inherent risk of third-party processing: Dotick can enforce data selection, authorization, and handling only within the boundary it controls and cannot guarantee absolute control over incidents, retention, or provider use outside that boundary. Legal details concerning responsibility, third-party processing, retention/training, and risk allocation must be formalized in the applicable Privacy Policy/Terms for the relevant release; the System Definition is not a substitute for legal terms.

The User must have a global control for disabling external AI processing. When disabled, AI-assisted Item Creation, Goal Discovery/AI Tag processing, and Daily Ring capabilities that depend on AI are unavailable; core Task/Event/Routine management, organization, collaboration, Offline behavior, and all other AI-independent capabilities must remain usable.

In the current pre-public baseline, the System Definition does not establish an independent product-level restriction regarding provider-side training use or retention policies for transmitted data. This subject must be formalized again at the relevant Security/Privacy gate before public release, but Current-Scope pre-public implementation must not be locked to a specific provider policy.

Speech-to-Text in the Voice flow may be local, platform-provided, or external. The System Definition does not commit to a transcription method; regardless of implementation, the transcript enters the same Dotick AI-assisted-creation semantics and validations.

## 9.3 Calendar / External Productivity Systems

Google Calendar, Notion, TickTick, and similar calendar/productivity systems are not operational sources of Dotick data within Current Scope. Dotick does not import Task/Event/Routine data from these services, perform bidirectional synchronization with them, or run automation based on their state within Current Scope.

These integrations belong to Future Scope. At this stage, no canonical direction is established for one-way import, two-way sync, ownership mapping, conflict authority, or automation policy. Such behavior becomes canonical only when the relevant integration is moved into an active Scope.

The presence of Source/provenance vocabulary or replaceable boundaries in the current model does not mean that these integrations are active.

## 9.4 Other Integrations

### Notification / OS Delivery

Notification and push delivery are within Current Scope. Dotick determines the Notification trigger, recipient, content, category, interaction state, and semantics; the OS or push-notification infrastructure only performs delivery/display within platform capabilities and policies. A delivery-provider limitation or failure must not change authorization or the domain meaning of the Notification.

### Email / Phone Messaging Infrastructure

Email and phone may be used in collaboration discovery to locate a destination Account. Discovery or sending a message does not itself create access or Membership, and Dotick continues to enforce the acceptance/authentication flow.

When adding an email address or phone number to an Account, Dotick must send the appropriate verification code and register that identifier as an active contact only after successful verification. An external email/SMS delivery service is responsible only for transporting the code or other messages. In verification, password-reset, or invitation flows, Dotick remains responsible for token/state, recipient matching, acceptance, authorization change, and the final outcome of the operation. Exact vendors and transport mechanisms belong to Design.

### Future External Agents and Voice Assistants

External AI agents and voice assistants such as ChatGPT, Claude, Gemini, Siri, Bixby, or Alexa are not integration clients within Current Scope. If added in the future, their access must be constrained by explicit User authorization, a defined Resource/capability scope, revocable permissions, and traceable audit. Adding such an integration must not imply exposing a public, unrestricted backend to arbitrary external clients.

---

# 10. Quality Expectations & Constraints

> This section records product-level expectations and constraints. Exact engineering metrics, SLAs, indexes, token expiry values, deployment tuning, and similar details are defined in specialized artifacts.

## 10.1 Security Expectations

Dotick must protect private User data and collaboration Resources according to effective authorization and field visibility. No client, realtime channel, Notification, export, or AI context may disclose information beyond the actor's valid access merely because that information exists in persistence.

Production network communications must use secure transport. Server-side data, operational backups, and device-local replicas must also use protection/encryption-at-rest appropriate to their environment. The System Definition does not lock a particular algorithm, key-management strategy, or storage mechanism, but storing credentials or sensitive data as unprotected plaintext in ordinary storage is unacceptable.

The current authentication baseline includes Email/Password, Google, and Passkey. Current Scope does not require TOTP, an SMS-based second factor, or mandatory enrollment in another independent 2FA mechanism. Adding such factors in the future requires a separate decision.

For collaboration discovery, username/name may support ordinary search, but lookup by email or phone must use exact or normalized-exact matching only. The lookup result must not reveal the destination User's private contact identifier to another actor; the system displays only the identity necessary to continue the collaboration flow.

`Platform Administrator` has full platform-level authority, but use of this bypass must be traceable. In addition to state-changing operations, Admin access to private User data must also be traceable in administrative audit. Retention, storage, and presentation details for this audit belong to Security/Audit Design.

## 10.2 Data Integrity Expectations

Dotick must prevent silent data loss. Every meaningful state change to persistent domain data must remain sufficiently traceable for conflict, recovery, and history to remain understandable. Current state may be changed or deleted when required by domain behavior, but the necessary historical trace must not disappear without an explicit policy.

Operations that logically modify multiple Resources together must produce a consistent outcome. If the complete consequence of a multi-Resource operation cannot be applied, the system must not treat a partially applied state as valid; the operation must fail atomically or be recovered atomically.

Offline reconciliation, concurrent edits, hierarchy moves, sharing/revocation, and delete/restore must not break ownership, placement, authorization, or identity invariants. Conflict resolution may replace one value with another, but the losing change must not disappear without an explainable history/recovery path.

Server-side User data must have appropriate backup/recovery for disaster or infrastructure failure so that failure of one deployment does not mean permanent loss of all operational data. Backup frequency, retention, RPO/RTO, and restore procedures belong to Operations/Security Design.

The User must be able to manually export their Account data. Export must be portable and machine-readable and must not silently omit core user-owned domain data. Exact format, packaging, and inclusion of files/Attachments are determined in the relevant Design. Current Scope does not require scheduled export, automatic external backup destinations, or import/restore from the same export.

### Account deletion and retention

The User must be able to request deletion of their Account. A deletion request places the Account into a 30-day retention/recovery window, during which the User must be able to cancel deletion and recover the Account.

After this window ends, the Account and personal operational data owned by that User must be permanently removed from active persistence. Sharing a personal Resource does not change its ownership; therefore, the User's personal Resources are also removed with their personal data at the end of the deletion lifecycle.

`Group-owned` Resources, or data owned by another actor/entity, are not deleted merely because the Creator's Account is deleted. Audit/history necessary to preserve integrity for other Users may remain after Account deletion using only the minimum necessary identity or in anonymized form.

Behavior of disaster-recovery backups after permanent Account deletion is defined in Security/Operations Design. The existence of a backup must not cause deleted data to return to ordinary accessible product state except through a controlled recovery permitted by the relevant policy.

## 10.3 Availability / Offline Expectations

Continuous network connectivity is not a prerequisite for core productivity behavior. A User who has previously authenticated validly must be able to open their authorized local working set Offline and continue the defined Offline-supported core flows for Task, Event, Routine, organization, and other supported capabilities.

There is no fixed product-level numerical expiry for Offline usage. Security/Session Design may require appropriate revalidation for server-dependent operations or at reconnect, but lack of connectivity alone must not make a valid local working set unusable after an arbitrary fixed number of days.

Failure or outage of an external dependency should remain isolated to the capability that depends on it as far as possible. AI failure must not disable manual productivity flow; Notification-delivery failure must not change domain state; and unavailability of an external identity provider must not unnecessarily invalidate an existing valid session or previously available Offline data.

Current Scope does not define a numerical uptime SLA. Time-driven lifecycles such as Dotick Day finalization or sync must be recoverable/idempotent when executed late so that execution delay does not change the meaning of the business boundary.

## 10.4 Historical Stability Expectations

Dotick must maintain a clear distinction between operational source state and historical/finalized artifacts. The User may correct old data in permitted flows, but that freedom must not silently rewrite a historical business record that was explicitly finalized by rule.

A finalized Daily Ring, closed statistical window, final score, and other finalized artifacts must preserve the meaning they had at the time of finalization. Later changes to title, Priority, Tag, schedule, relation, or other source-Item fields must not transform the historical snapshot into current state.

History must preserve meaningful versions and branches created from historical checkout/restore without rewriting the previous path. Delete/Reset and conflict resolution must likewise preserve the trace needed to explain current state so that recovery and audit remain dependable.

Explicit permanent deletion, including the end of Account or Trash retention, is a controlled exception to preservation of operational state; it must not be confused with ordinary edit behavior or implicit cleanup.

## 10.5 Performance Expectations

Core daily interactions such as navigation, opening an Item, editing a field, changing state, and working with the local working set should feel responsive and should not unnecessarily wait for network access or heavy computation.

Expensive work such as AI inference, semantic analysis, broad synchronization, statistics refresh, or recomputation should be separated from the synchronous interaction path, deferred, or executed asynchronously whenever semantics permit. This principle does not allow consistency or domain correctness to be sacrificed for apparent speed.

Feature richness is preserved by default. Simplifying or deferring behavior is justified when real measurement demonstrates that the behavior causes noticeable and recurring degradation in User experience. Speculative optimization must not be used as a reason to remove capabilities prematurely.

The System Definition does not specify numerical latency budgets or throughput. Acceptance thresholds, benchmark targets, and performance budgets for individual flows are defined in Performance/Test Specifications.

## 10.6 Other Product Constraints

### Current client

Current Scope supports a **responsive, installable Progressive Web Application (PWA)** as the official User-facing client. The same PWA must be usable in supported browsers on desktop and mobile, and installability is part of the current experience.

The PWA must be able to use browser/platform-supported notification/push capabilities for Current-Scope Notifications. If a specific platform does not support a native/web capability, that capability may degrade or be unavailable on that platform; the limitation must not change the shared Notification or domain-data semantics for the same User.

Native Android/iOS applications, desktop-native clients, OS widgets, and other platform-specific clients are not committed within Current Scope and remain in Future Scope.

### Hosting boundary

Current Scope does **not** include supported self-hosting for arbitrary end Users. Publishing source code or making a development environment runnable does not by itself imply providing a self-hosting package, deployment contract, operational documentation, or access to Dotick-managed secrets/configuration.

Dotick is not required to deliver Current Scope in a form that allows every User to operate a fully supported production instance on an arbitrary server. Local/development deployment belongs to the Engineering/Deployment workflow and is not a product capability.

### Language and user content

The product interface language within Current Scope is **English**. Full UI localization into other languages is not a current requirement.

User-generated content, however, must support storage and display of Persian text in title, description, Comment, Note, and other permitted textual fields. Presentation must select appropriate fonts based on displayed-content language so that English and Persian text are each rendered with suitable typography. Exact font families, language-detection mechanisms, and typography rules belong to UI/UX Design.

### Cross-client semantics

Browser, PWA, or platform limitations must not alter the shared meaning of domain data. If a particular capability cannot be provided in an environment, degradation must occur in that capability's presentation/delivery, not by defining different status, ownership, schedule, completion, or authorization semantics.

---

# 11. Assumptions & Dependencies

> This section records environmental assumptions and dependencies on which Current-Scope behavior relies. The existence of a dependency does not make that dependency a domain source of truth. Failure of each dependency must be handled according to the boundaries defined in Sections 8, 9, and 10.

## 11.1 Assumptions

### Verified contact ownership

Dotick does not assume that every entered email address or phone number belongs to the User who entered it. A contact identifier may be added to the Account only after successful verification. Verification occurs through a code sent to the same email address or phone number. An unverified value is not retained as an active contact and cannot be used for discovery, invitation targeting, or flows that depend on a contact identifier.

### Supported PWA environment

The current client is an installable PWA and relies on persistent local storage that is usable in the browser/platform for a complete Offline experience. If the environment, quota, or browser mode does not allow sufficient local persistence, Dotick must preserve Online functionality as far as possible, degrade Offline capability to the level actually available, and inform the User about the local-data limitation. Insufficient local storage alone must not make the entire application unusable.

### Platform permissions are optional delivery capabilities

Notification permission may be denied by the User or revoked later. Dotick must not make the availability of other product capabilities dependent on this permission. Reminder/Notification state may remain valid in the domain, but delivery outside the application does not occur without permission, and undelivered Reminders are not accumulated in the Notification Center as compensation.

Voice AI creation depends on microphone capability and permission. If permission is unavailable, the system does not assume that a Text-AI alternative exists; the User must enable microphone permission or use manual Item creation.

### User-provided AI credential responsibility

If the User provides a personal AI credential/API, Dotick assumes the User has the right to use that credential and is responsible for the corresponding provider Account, quota, billing, and contractual restrictions. Dotick does not guarantee availability or cost of the personal provider, and credential failure follows the defined service-managed fallback behavior.

### Local device clock is not authoritative

Dotick must not assume that the device's local wall clock is always accurate or trustworthy. Local device time may be recorded as input while Offline, but change ordering, conflict resolution, authorization, and history integrity must not depend solely on the timestamp asserted by that device. Abnormal clock skew must not silently cause data loss, false historical ordering, or an incorrect write to win. The exact clock/reconciliation strategy belongs to Sync Design.

### Eventual connectivity for server-dependent behavior

Core Offline flows do not require continuous connectivity for local execution, but convergence across devices, server-side authorization, collaboration management, backup, downloading non-local files, and capabilities dependent on external services ultimately require valid connectivity.

## 11.2 Dependencies

### Dotick backend and server-side state

Account state, authoritative collaboration/authorization, central synchronization, server-side persistence, backup/recovery, remote Attachment storage, and online-only operations depend on the Dotick backend. The local replica is operationally valid while Offline but is not a permanent replacement for the server as the point of convergence and current authorization.

### Browser / PWA capabilities

The Current-Scope experience depends on supported browser/platform capabilities including:

- persistent local storage for the Offline working set and pending changes;
- installability required by the PWA;
- notification/push capability for delivery outside the application;
- microphone access for Voice AI-assisted creation.

Absence of an optional platform capability must degrade only the dependent feature, not shared domain semantics.

### Email and SMS delivery

Adding an email address or phone number to an Account depends on successful delivery of a verification code and User confirmation. Email verification, password reset, and invitation transport may also depend on email/SMS infrastructure. The external provider only performs delivery; validation, contact state, authorization, and invitation state remain owned by Dotick.

### Google authentication

Google is a dependency only for a User who chooses Google authentication. A Google outage must not destroy Account data or a valid Offline session; new login for an Account without an independent fallback may remain limited until the provider returns.

### AI and Speech-to-Text execution

Voice AI-assisted creation, Goal Discovery/AI Tag processing, and Daily Ring behaviors dependent on AI require valid AI execution. Speech-to-Text may be local, platform-provided, or external, but the Voice flow requires a valid transcript in every case. Failure of these dependencies must remain limited to the dependent capability according to AI Failure Behavior.

### Device-local Attachment cache

Attachment cache is independent per device. After upload, the server-side Attachment is the durable source of the file, while the local binary is only a manageable copy/cache on that device.

A file uploaded from the same device remains openable without re-downloading while its local copy exists. On another device, the binary must be downloaded unless an auto-download policy has already fetched it.

The User must be able to define a device-wide cache policy and override it for a specific Folder or List. At minimum, policy must control automatic download, retention duration including indefinite retention, and maximum local cache size. Cleanup due to retention or capacity removes only the local binary; the server-side Attachment and its metadata remain available and can be fetched again when connectivity exists.

### Time reconciliation

Sync and History flows depend on temporal/ordering metadata that can reconcile changes even when device clocks are skewed. The exact mechanism—including server time, logical ordering, hybrid strategy, or equivalent metadata—is defined in Sync Design, and the System Definition does not lock a particular clock algorithm.

---

# 12. Out of Scope / Future Scope

## 12.1 Explicitly Out of Current Scope

The following are not within Dotick's Current Scope:

- customized organizational roles and Custom Roles;
- organizational structures and hierarchies based on a person's formal position in a company;
- visibility rules, team/department management, and administration that depend on organizational governance;
- public social-network capabilities such as follow/follower relationships, public feeds, standalone Public Profiles, social graphs, and public User/content discovery outside a specific collaboration action;
- payment, paid subscriptions, billing, and other financial transactions;
- TOTP/SMS-based second-factor authentication as an additional independent factor;
- supported self-hosting and production deployment for arbitrary end Users;
- typed-text AI-assisted Item creation for direct User input; typing in the Current Product is ordinary manual creation;
- a general-purpose public developer API for arbitrary third-party clients;
- full UI localization into Persian or other languages;
- a formal, standardized accessibility baseline for the current release;
- direct integration with third-party calendar/productivity systems;
- native mobile/desktop clients, OS widgets, and other clients beyond the current PWA.

An optional `Profile Picture` for an Account is an exception to the social-network boundary above. A Profile Picture is only part of User identity presentation in valid Dotick contexts such as collaboration discovery, Share/Group requests, Member lists, Comments, and Assignments. It does not create a public page or an independent social-discovery surface.

Within Current Scope, discovery for Direct Sharing or Group invitations may use username/handle, name/display name, email, and phone. This behavior is purpose-specific and is not a public social network.

There is no fixed product-level limit on the number of members in a Group. The boundary between Current Scope and Enterprise Scope is determined by the need for organizational governance and authorization, not merely by member count.

Capabilities that are not within Current Scope are not necessarily `Future Commitments`. Capabilities such as a public social network, supported self-hosting, direct User typed-text AI input, a general-purpose public API, full UI localization, and additional TOTP/SMS 2FA are not part of the currently planned product direction and may enter Future Scope only through a new canonical decision.

## 12.2 Future Enterprise Scope

Future Enterprise Scope includes capabilities that transform Dotick from a personal/group product into a system with organizational governance, including:

- `Organization/Tenant` and tenant isolation;
- Custom Roles and arbitrary permission composition;
- formal organizational structure and hierarchy;
- manager/subordinate visibility;
- team and department management based on organizational structure;
- Enterprise SSO after an appropriate protocol is selected;
- organization-level administration, policy, and reporting;
- organizational privacy/compliance requirements that depend on Enterprise context.

Adding Enterprise capabilities must not make the baseline semantics of Personal Accounts, Direct Sharing, or non-organizational collaboration dependent on organizational hierarchy.

## 12.3 Future Integrations

Direct connections to external calendar/productivity services and external integration clients are outside Current Scope and remain Future Scope. This limitation does not apply to Current-Scope external dependencies such as Google Authentication, external AI inference, email/SMS delivery, or OS/push-notification infrastructure.

Known Future Integrations include:

- Google Calendar;
- Notion;
- TickTick;
- other calendar and productivity services;
- Email and other external sources as inputs to automation/creation pipelines beyond current delivery/invitation usage;
- AI agents such as Claude or ChatGPT acting on Dotick under explicit User authorization;
- voice assistants such as Gemini, Siri, Bixby, and Alexa;
- Trusted Automation, in which an action may execute without per-action confirmation only within explicit, scoped, revocable, and auditable User authority.

Future external integrations must use a controlled, permission-based integration surface. In the current product direction, Dotick does not define a general-purpose public developer API for arbitrary external clients as a Future commitment.

Typed text arriving from a future external source, such as Email, into an automation pipeline is not the same capability as direct User typed-text AI creation. The Voice-only decision for direct User-triggered AI input remains in effect.

Sync direction, authentication, conflict handling, trusted-automation levels, and integration contracts will be defined in future specialized artifacts.

## 12.4 Other Future Capabilities

The following are recognized Future directions for Dotick, but Current-Scope acceptance does not depend on them:

- advanced AI personalization and adaptation using correction history and recorded behavioral signals;
- stronger accessibility support for a mature/public product stage, including capabilities such as keyboard accessibility, screen-reader semantics, scalable text, and appropriate contrast; the exact standard/level must be selected before it becomes a requirement for the corresponding release;
- a dedicated desktop application;
- native or platform-specific mobile/desktop clients when justified by product need;
- OS/application widgets;
- deeper platform-specific capabilities beyond Current-Scope Notification delivery, including complete persistent/alarm-like behavior using native APIs for each OS, full-screen alarms/background scheduling, and platform-specific interactions.

Future commercialization is likely, but the monetization model is not yet a finalized product decision. Pricing, subscriptions, licensing, billing, or payment flows must not be treated as Future commitments or architectural constraints until a separate Business/Product decision establishes them.

Full UI localization, additional TOTP/SMS 2FA, supported self-hosting, a public social network, direct User typed-text AI input, and a public developer API are not currently Planned Future Capabilities. Their absence from Current Scope must not be implicitly interpreted as a promise that they will be added in future versions.

The existence of these Future capabilities does not mean the Current-Scope architecture must anticipate or lock in a dedicated implementation for all of them from the beginning. Current boundaries should simply avoid unnecessarily blocking reasonable evolution.

Any new capability whose Scope status is unclear may first be analyzed/rationalized in the Decision Register, but it does not become canonical behavior until the result is recorded in the System Definition. After current behavior is recorded here, the Decision Register and SRS must be reconciled with it.

---

# 13. Intentionally Unspecified Current-Scope Design Details

> At the level of concepts, Scope, and overall Current-Scope behavior, no Product/Domain decision should remain unresolved.
>
> If a subject still requires a product or domain decision, it may be analyzed in the `Decision Register`, but the result becomes canonical current behavior only after it is recorded in the appropriate behavioral section of the `System Definition`; the Decision Register/SRS are then reconciled with it.
>
> This section contains only **Current-Scope** details whose high-level behavior is already defined but whose exact implementation, representation, tuning, or formula is intentionally delegated to the owning Design/Specification artifact. Enterprise/Future details are not listed here.

## 13.1 Intentionally Unspecified Implementation Details

The following have defined Current-Scope behavior, but their exact representation or implementation is intentionally not locked by the System Definition:

- the physical schema, serialization, ordering, and edit-storage model of `RichDescription` and `ContentBlock`, while preserving stable block identity and the defined Comment/Reference behaviors;
- the exact schema and indexing of structural-child, dependency, and normal-reference relations, provided that queryability, cycle rules, and finalized semantics are preserved;
- the exact representation and persistence of Recurrence Rules, series/occurrence identity, exceptions, and overrides, while preserving recurrence historical stability and edit/delete semantics;
- endpoints, payloads, API versioning, and transport contracts, provided that they do not alter canonical behavior or authorization;
- sync metadata, device identity, ordering/clock strategy, idempotency representation, conflict metadata, and the exact representation of delete/edit conflicts;
- verification-code format, expiry, retry/rate-limit, anti-abuse mechanisms, and exact email/phone normalization;
- internal representation of Attachment-cache policy, cache accounting, eviction ordering, quota handling, and browser/platform storage APIs;
- encryption-at-rest algorithms/standards, key management, and the exact mechanism for protecting server-side and client-side storage;
- backup frequency, retention, RPO/RTO, verification, and restore procedures for disaster recovery;
- the exact format and packaging of manual User-data export, including how Attachments are packaged;
- session-hardening mechanics, the exact Account-linking flow, and credential-recovery mechanics;
- storage/protection of personal AI credentials, internal routing among service-managed providers, timeout/retry policy, and the exact implementation of STT/provider integration;
- detailed PWA implementation, including service workers, installability mechanics, Offline storage strategy, and supported browser/version matrix;
- detailed Notification transport/provider behavior, device registration, and delivery-retry mechanics, without changing Reminder/Notification semantics;
- exact schema/index/ORM mapping and persistence strategy for entities, history branches, and derived states, except where a technical constraint has already become canonical;
- the exact implementation of Profile Picture storage, resizing/derivative generation, and delivery, without turning it into a Public Profile capability;
- the exact representation and implementation of Time Semantics, subject to creation of a dedicated specification that analyzes the interactions among real instants, Calendar Day, Dotick Day, `RoutineCompletion.occurrence_date`, credited/effective date, all-day intervals, Account/device timezone, DST, Jalali/Gregorian recurrence, leap/invalid dates, and the finalization boundary. That specification must define comprehensive test vectors and test cases for boundaries and combinations of these parameters.

These matters must be resolved in their relevant Design/Specification artifacts and must not change canonical product behavior merely to simplify implementation.

## 13.2 Intentionally Unspecified Algorithms / Formulae

The behavior and objective of the following Current-Scope capabilities are defined, but their exact values, coefficients, thresholds, or algorithms intentionally remain tunable:

- the exact `Daily Ring` progress/final-score formula and scoring coefficients;
- early-completion bonus and late-day-recovery tuning;
- the exact Goal-selection algorithm and weights, signal normalization, and learning/adaptation parameters, while preserving balanced-selection behavior;
- the exact method for estimating and numerically representing difficulty/effort;
- `Adaptive Norm` thresholds, windows, and rate of change;
- the inactivity threshold and decay curve for incremental Routine, while preserving the baseline floor and confirmed behavior;
- the exact initial warm-up duration for AI Goal Discovery;
- numeric/model-specific thresholds for Goal similarity, merge, and reactivation;
- the exact timing, frequency, cooldown, and copy of motivational/scolding behavior;
- the exact frequency/rate limit of Goal-level motivational Reminders;
- prompt templates, model-specific parameters, and detailed AI evaluation/tuning, provided that authority, review requirements, and all other product semantics remain unchanged.

None of these items should be interpreted as an unresolved Product Decision. Algorithm or tuning changes are permitted only when they preserve the canonical behavior and constraints defined in this document.

---

# 14. Glossary / Terminology

This Glossary records the canonical meanings of terms that have domain-specific meanings in Dotick or may otherwise be incorrectly conflated across documents. The definitions in this section summarize behavior already established elsewhere in this document and do not create new requirements or behavior.

## 14.1 Dotick-specific Terms

| Term | Canonical meaning |
|---|---|
| `Dotick Day` | Dotick's logical day, whose boundary is determined by product rules and is not necessarily the same as a Calendar Day from 00:00 to 24:00. Once created, each Dotick Day has its own fixed time interval. |
| `Daily Ring` | The daily plan for a Goal, intended to produce meaningful and achievable progress within one Dotick Day. A Ring consists of RingGroups and DailyActions and becomes a historical snapshot after finalization. |
| `RingGroup` | A group of DailyActions within a Daily Ring that has a specific contribution or satisfaction rule, such as all-members, minimum-count, minimum-credit, one-of-many, credit-cap, or hard-requirement behavior. |
| `DailyAction` | A snapshotted daily action representing either full completion of an Original Item or a meaningful, measurable portion of it for the same Dotick Day. A DailyAction is not necessarily an independent Item. |
| `Global Streak` | The User's global daily streak. On evaluable Dotick Days it continues when at least one Daily Ring is completed. Days with no valid evaluable Ring opportunity are paused according to the relevant rules. |
| `Goal Discovery` | Dotick's intelligent capability for identifying and lifecycle-managing Goals and AI Tags from the User's authorized context. Goals in this flow are not manually created by the User. |
| `AI Tag` | A Tag created and lifecycle-managed by the intelligent Goal/Tag process. Unlike a User-created Tag, individual rename/delete management is not controlled by the User. |
| `Service-managed AI` | AI execution mode in which Dotick manages the provider, model/route, and required credentials according to service policy; the User does not directly select the provider/model. |
| `Personal AI Credential` / `BYOK` | The User's personal credential or API key for a supported provider. When this mode is selected, Dotick first uses the User's credential, and its failure may fall back to Service-managed AI according to the defined policy. |
| `External AI Processing Control` | A global User setting that disables capabilities dependent on external AI processing without disabling core productivity behaviors that do not depend on AI. |

## 14.2 Domain Terms

| Term | Canonical meaning |
|---|---|
| `Account` | The registered internal Dotick identity to which authentication methods, profile/account state, and User ownership/access are attached. An external identity provider does not replace the internal Account. |
| `Registered Personal User` | The base human user class in Current Scope. Direct Collaborator, Group Member, and collaboration Manager are contexts of the same Account, not separate Account types. |
| `Resource` | A general term for an entity that may have independent ownership, access, history, sharing, or lifecycle. The specific behavior defines which Resources are eligible in that context. |
| `Item` | The conceptual root of primary productivity content: Task, Event, and Routine. Goal is not an Item. |
| `Schedulable` | A conceptual capability shared by Task and Event for schedulable behavior. The term does not require physical or ORM inheritance. |
| `Task` | An Item representing work to be performed and that may have schedule, deadline, dependency, priority, and Task-specific lifecycle behavior. |
| `Event` | An Item that may be unscheduled, timed, or all-day. Its time-driven lifecycle `Not_Arrived / Ongoing / Finished` applies only after a valid start schedule exists. |
| `Routine` | The recurring definition of a behavior or activity. Routine has no independent daily status; each day's outcome is recorded in RoutineCompletion. |
| `RoutineCompletion` | The current progress/outcome state of a Routine for a specific `occurrence_date`. Absence of a RoutineCompletion means no outcome/progress has been recorded. |
| `Folder` | The highest optional container in the Current-Scope organization hierarchy. A Folder contains Lists, and nested Folders are not supported. |
| `List` | The primary Item container in the organization hierarchy. It may appear inside a Folder or independently in the User experience and contains Columns. |
| `Column` | The lowest organization container in `Folder > List > Column`. Each Task/Event is located in exactly one Column of its List. |
| `Inbox` | The special, permanent List of every Registered Personal User and the default destination for Task/Event creation. The User cannot rename or delete it. |
| `Goal` | A semantic objective independent from the Item hierarchy, created and managed by AI-managed Goal Discovery and used as the basis for Daily Rings. |
| `Tag` | An independent entity used for labeling and semantic association. A Tag may be User-created or AI-created, and its relation to Items is many-to-many. |
| `TrackingState` | Shared capability/state for tracking metrics such as streak and total completions. It does not imply a shared physical superclass. |
| `RichDescription` | The block-based Description used by Task/Event and composed of ContentBlocks with stable identity. |
| `ContentBlock` | A stable-identity unit inside RichDescription that may represent content such as Text, Attachment, Location, or Item Reference and may be the target of a Comment. |
| `Structural Parent / Child` | A real hierarchy relation among Task/Event. Each Item has at most one structural parent, cycles are prohibited, and the relation affects placement/move/delete behavior. |
| `Reference` | A non-structural reference to an Item from within RichDescription. A Reference does not create a structural parent and may exist in multiple contexts. |
| `Dependency` / `Blocker` | A relation between Tasks in which a dependent Task cannot become Done until the blocker becomes Done. Dependency is independent from structural hierarchy. |
| `Recurrence` | The rule for producing recurring occurrences using the calendar and granularity allowed for the entity. Historical occurrences are not rewritten when a future rule changes. |
| `Occurrence` | A temporal/date instance belonging to a recurrence series or an evaluable Routine day, depending on entity context. |
| `Reminder` | An explicit reminder request associated with an Item/Goal whose trigger and semantics are managed by Dotick; the external delivery channel is not part of the Reminder's meaning. |
| `Assignment` | The responsibility relation indicating one or more Users with access who are responsible for performing a Task. Assignment alone does not create authorization. |
| `Claim` | An action by an authorized actor to accept responsibility for a Task. Like Assignment, it does not create access. |
| `Direct Sharing` | Granting controlled access to a specific Resource without requiring GroupMembership. |
| `Access Profile` | A predefined preset of authorization capabilities for Direct Sharing, such as Viewer/Commenter/Contributor/Manager. |
| `Group` | A persistent multi-user collaboration context with Membership, System-defined Roles, and shared Resources. Group is not a mandatory primitive for all Sharing. |
| `GroupMembership` | The membership relation of a Registered Personal User in a specific Group, activated through User acceptance and carrying that Group's Role. |
| `System-defined Role` | A predefined preset of Group capabilities within Current Scope. Custom Roles do not exist in Current Scope. |
| `Group-owned Resource` | A Resource created directly in a Group context and owned by the Group. The Creator leaving the Group does not change its ownership. |
| `Group-scoped Personal Resource` | A personal Resource placed into a Group context without transferring ownership. While in that context, it follows the Group's authorization rules. |
| `Effective Access` | The actor's actual permission set on a Resource after accounting for ownership, Direct Share, inherited access, Group context, and other valid access paths. |
| `Field Visibility` | A user-facing restriction on which groups of Resource information an authorized actor may view. It is not the same as internal storage/sync/audit metadata. |
| `Inherited Access` | Access propagated from a Shared container to its descendants, such as Folder to List/Item or List to Item. |
| `Source` | The provenance of a Resource/Item, describing where the data came from and remaining independent from owner, Creator, and authorization. |
| `Finalization` | The transition of a derived/open period state into a closed historical business record according to a defined lifecycle, such as the end of a Dotick Day or statistical window. |
| `Finalized Artifact` | A derived artifact that is no longer rewritten by later edits to source data after finalization, even though the source Item itself may remain editable. |
| `Historical Snapshot` | A fixed representation of past state/decision whose meaning must not be rewritten by future changes to source data. |
| `Trash` | The recoverable deletion lifecycle for eligible Resources, with a current retention period of 30 days before permanent deletion. |
| `Local Replica` | The local, editable copy of User state required on a device/PWA for core Offline flows; it is not merely a read-only cache. |
| `Reconciliation` | The process of converging local changes with authoritative server state after connectivity and propagating the final state to other replicas. |
| `Field-level LWW` | The baseline field-level conflict-resolution strategy that determines a winning write independently for each field. The exact clock/metadata mechanism is a Design concern, and device clock alone is not authoritative. |
| `Calendar Day` | A calendar day in the effective calendar/timezone, usually midnight to midnight. It must not be assumed to be the same as a Dotick Day. |
| `Account Timezone` | The timezone stored on the Account and used for presentation and future time resolution. It is not silently overwritten when the device timezone changes. |
| `Credited / Effective Date` | The Dotick Day or business date to which a completion/action is attributed for streak, scoring, or day-based statistics. It may be independent from the raw event timestamp. |
| `Profile Picture` | The optional User identity image shown in valid Dotick contexts such as collaboration. Its existence does not create a Public Profile or social-network surface. |
| `Attachment Cache` | The device-specific local binary cache for Attachments. Removing a cached binary does not delete the server-side Attachment, and cache policy may be global or overridden at Folder/List level. |

## 14.3 Legacy / Deprecated Terms

| Legacy / Deprecated term | Current interpretation |
|---|---|
| `Tab` | Legacy name for `Column`. It is not an independent entity and must not be used as a separate layer in current terminology. |
| `Section` | Legacy name for `Column`. It is not an independent entity. |
| `not_sectioned` | Technical/legacy name for the default state or default Column in older models. It must not be used as an independent user-facing concept. |
| `DailyRingItem` | The previous representation of a Daily Ring as flat Item membership. The current model uses `RingGroup` and `DailyAction`; the historical-snapshot principle remains preserved. |
| `Speech-to-Task` | An older, overly narrow framing of AI-assisted creation. Current Scope uses Voice AI-assisted creation for Task, Event, and Routine proposals. |
| `Text + Voice AI-assisted Item Creation` | Older wording that treated Text as a current AI-creation modality. Current Scope supports only Voice for User-triggered AI-assisted creation. |
| `Trackable` | An older inheritance-oriented interpretation of metrics shared by Routine/Goal. The current term is `TrackingState` as a shared capability/state. |
| `Routine status` | The older model that assigned Routine a global status. Routine has no status; daily state exists in `RoutineCompletion`. |

---

# Appendix A — Document Responsibility Boundaries

```text
Decision Register
= Why was this decision made?
  What alternatives existed?
  What were the trade-offs?
  How and why was the decision finalized?

System Definition
= What is the system now?
  What is in Scope?
  What concepts does it contain?
  How must it behave?

Domain Model
= What are the concepts, entities, value objects, relationships, and conceptual constraints?

Formal SRS
= How are the defined behaviors converted into formal, atomic, identifiable, and testable requirements?

Design
= How are these behaviors implemented?
```
