# Increment 1 Folder/List/Column Navigation Model

> **Status:** Formal analysis artifact for Increment 1; this document does not assert implementation completion.
>
> **Date:** 2026-09-11
>
> **Authority:** System Definition §6.1 and related ownership rules → Decision Register (`DR-001`, `DR-096`) → SRS §3.1 (`SRS-ORG-001..006`) → this analysis artifact.
>
> **Increment boundary:** `SRS-ORG-001..005` are Increment 1 organization requirements. `SRS-ORG-006` owns the later full main-navigation presentation in Increment 5. This document defines organization/navigation semantics required by I1 without locking the final sidebar, bottom bar, view switcher, responsive layout, or other I5 presentation choices.

## 1. Purpose

This model defines how a personal Dotick user navigates the Increment 1 organization hierarchy and how navigation context maps to valid Item placement.

The canonical organization hierarchy is:

```text
Personal organization root
├── Inbox
├── Folderless List
│   └── Column
└── Folder
    └── List
        └── Column
```

At the domain level, the canonical terminology remains:

```text
Folder
└── List
    └── Column
        └── Item
```

`Folder` is optional in the user experience. `List` and `Column` are the mandatory placement hierarchy for placed Task/Event items. In Increment 1, only Basic Task behavior is implemented from that Item set.

## 2. Scope

This Increment 1 navigation model covers:

- Inbox as the default organization destination;
- optional Folder grouping;
- Folderless Lists;
- Lists and their Columns;
- the mandatory default Column of every List;
- hiding the technical/default Column concept when it is the only Column;
- navigation-context resolution for Task creation and movement;
- personal ownership isolation for Folder/List/Column discovery and selection.

The following are deliberately outside this I1 model:

- final primary-navigation UI structure, placement, gestures, responsive behavior, or navigation chrome (`SRS-ORG-006`, Increment 5);
- List/Kanban/Timeline presentation switching;
- Calendar and Today view behavior beyond the organization concepts needed by I1;
- Group-owned/shared Folder/List/Column navigation and authorization (Increment 7);
- offline navigation/sync conflict behavior (Increment 6);
- structural child/hierarchy navigation (Increment 2);
- Event-specific navigation behavior (Increment 2);
- Routine placement, because Routine does not use Folder/List/Column placement.

## 3. Canonical nodes and roles

| Node | Role in I1 navigation | Placement role |
|---|---|---|
| Personal organization root | Logical root of the authenticated User's private organization tree. It is not an Item placement target. | None |
| Inbox | Special first-class destination used when Task creation does not specify another placement. | Resolves to the User's Inbox/default Column |
| Folder | Optional grouping container for Lists. A List may exist without a Folder. | Not a direct Task placement target |
| List | Required organizational parent of Columns. May be folderless or grouped under one Folder. | Placement context only after a Column is resolved |
| Column | Required direct placement container for I1 Tasks. Every List has at least one default Column. | Direct Task placement target |
| Task | I1 user-facing Item navigated within its owning Column/List context. | Exactly one Column |

### 3.1 Folder is optional

A User must be able to have a List without placing that List inside a visible Folder. If an implementation uses a hidden/default Folder internally to normalize persistence, that hidden implementation detail must not become a required user-facing navigation node.

Therefore the visible path to a List is either:

```text
List
```

or:

```text
Folder / List
```

A User must not be forced to create, select, or manage a Folder merely to create or use a List.

### 3.2 List is the stable organizational context

A List owns one or more Columns. A Folder groups Lists but does not replace the List/Column placement model.

A Folder selection may expose or organize its contained Lists, but "place Task in Folder" is not a complete placement operation. Before persistence, a Task destination must resolve to a concrete Column belonging to a concrete List.

### 3.3 Column is the direct placement unit

Every List must have a default Column. A Task placed in a List without an explicit Column resolves to that List's default Column.

When a List has multiple visible Columns, an explicit Column may be selected as the destination. The exact I5 visual presentation of those Columns is not defined here.

### 3.4 Technical default Column is not a separate user concept

The legacy/technical name `not_sectioned` may represent the default state/default Column internally, but it is not an independent entity and must not be exposed as a required user-facing concept.

If the default Column is the only Column in a List:

- the User may navigate directly to the List without seeing a separate technical Column label;
- Task creation in that List implicitly resolves to its default Column;
- the hidden presentation does not remove the underlying Column placement invariant.

If additional Columns exist, the UI may expose Column distinctions according to the relevant design, while they remain the same canonical `Column` entity type.

`Tab` and `Section` are legacy names for `Column`; they must not appear as separate domain/navigation entity types.

## 4. Inbox model

Inbox is a special root-level navigation destination for the authenticated User. It provides the default place for an I1 Task when the User does not choose another List/Column during creation.

The navigation model requires the following behavior:

1. Inbox is available without requiring the User to create a Folder or ordinary List first.
2. Inbox resolves to a concrete owned List/Column placement in persistence/API terms; Tasks are not stored with an undefined organization parent.
3. Creating a Task from a global/default creation context without an explicit destination places it in the User's Inbox/default Column.
4. Navigating to Inbox displays only resources visible within the current User's Inbox scope.
5. Inbox is special product behavior, not a substitute name for every default Column in every List.
6. A normal List's default Column and the Inbox/default Column follow the same mandatory-Column invariant, but they remain different organization destinations.

The physical representation of Inbox is a design/persistence concern. This analysis defines its navigation semantics rather than requiring a competing storage model.

## 5. Navigation context model

I1 navigation maintains an **organization context** describing what the User is currently operating within. The minimal semantic contexts are:

```text
InboxContext
ListContext(list_id)
ColumnContext(list_id, column_id)
FolderContext(folder_id)   # organizational browsing only
```

These are analysis concepts, not required API schema/class names.

### 5.1 InboxContext

`InboxContext` means:

- the current destination is Inbox;
- implicit Task creation resolves to the User's Inbox/default Column;
- only the authenticated User's Inbox resources are queryable.

### 5.2 FolderContext

`FolderContext` means:

- the User is browsing one owned Folder and its owned Lists;
- the Folder itself is not a direct Task placement target;
- Task creation must resolve to a List/Column before persistence, unless the creation flow explicitly falls back to Inbox outside the Folder action.

This document does not require a specific Folder landing-screen layout.

### 5.3 ListContext

`ListContext(list_id)` means:

- the User is operating in one owned List;
- if a Task creation action omits a Column, placement resolves to that List's default Column;
- if the default Column is the only Column, the UI may present the List as a single flat destination while persistence still uses the default Column;
- if multiple Columns exist, they remain child destinations of that List.

### 5.4 ColumnContext

`ColumnContext(list_id, column_id)` means:

- the selected Column must belong to the selected List;
- both resources must be inside the authenticated User's I1 ownership scope;
- Task creation/move using this context resolves directly to that Column.

The server must not trust a client-supplied `list_id`/`column_id` pairing without validating the relationship and ownership.

## 6. Selection and navigation rules

### NAV-01 — Root discovery is owner-scoped

The authenticated User's organization root may expose only the User's private I1 organization resources. Knowledge of another User's Folder/List/Column UUID must not make it navigable or discoverable.

### NAV-02 — Folder expansion cannot change domain placement

Expanding/collapsing or selecting a Folder is presentation/navigation state only. It does not move Tasks or change List ownership/placement.

### NAV-03 — Folderless Lists remain first-class

Lists without a visible Folder must remain directly navigable from the personal organization root or an equivalent I5 presentation. Navigation design must not make Folder membership a prerequisite for accessing a List.

### NAV-04 — List selection resolves its Column invariant

Selecting a List establishes the List context. When no explicit child Column is selected for an I1 placement action, the List's default Column is the placement target.

### NAV-05 — Column selection is always List-relative

A Column is navigated within its owning List. A client must not compose a Column from one List with a different List context and expect the server to accept the destination.

### NAV-06 — Inbox is the destination of omitted global placement

When I1 Task creation occurs without an explicit List/Column destination, the organization context resolves to Inbox/default Column rather than leaving placement null.

### NAV-07 — Technical aliases do not create navigation nodes

`Tab`, `Section`, and `not_sectioned` must not create additional entity levels alongside `Column`.

### NAV-08 — Hidden sole default Column preserves semantics

If a List contains only its default Column, hiding the Column label/control in the UI must not change storage, ownership, move, or creation semantics. All affected Tasks still resolve to that concrete default Column.

### NAV-09 — Navigation cannot bypass ownership validation

Client-side visibility or previously cached navigation state is not authorization. Every server-side read or write involving Folder/List/Column identifiers must re-establish the authenticated User's allowed scope.

### NAV-10 — Final navigation chrome remains deferred

This model does not decide whether I5 uses a sidebar, bottom bar, drawer, gestures, breadcrumbs, tabs, or another responsive mechanism. Such choices may represent the same organization model without changing domain data.

## 7. Placement resolution table

| User action/context | Resolved I1 Task placement |
|---|---|
| Create Task with no destination | Inbox → Inbox/default Column |
| Create Task while explicitly targeting Inbox | Inbox → Inbox/default Column |
| Create Task in a List, no Column specified | Selected List → that List's default Column |
| Create Task in an owned explicit Column | Selected List → selected Column |
| Attempt creation with Folder only | Incomplete direct placement; a List/Column must be resolved before persistence |
| Attempt creation/move to foreign List/Column | Reject without cross-user disclosure |
| List has only hidden default Column | Resolve to the same concrete default Column; UI may omit its technical label |

## 8. Canonical navigation paths

The following path shapes describe semantic ancestry, not URL requirements:

```text
Inbox

List
└── Default/Selected Column

Folder
└── List
    └── Default/Selected Column
```

A Task's organization ancestry in I1 is therefore one of:

```text
Inbox / Inbox-default-Column / Task
```

or:

```text
List / Column / Task
```

or, when the List is visibly grouped:

```text
Folder / List / Column / Task
```

Folder presence in the visible path does not alter the fact that the Task's direct placement is the Column.

## 9. Error and stale-navigation behavior

The I1 model must tolerate navigation state becoming stale between client rendering and server action.

- If a referenced Folder/List/Column no longer exists or is not accessible to the current User, the server returns the normal inaccessible/not-found surface rather than leaking ownership details.
- If a cached Column no longer belongs to the supplied List, the server rejects the destination relationship.
- A failed destination validation must not silently create/move a Task into Inbox unless the product action itself was explicitly an Inbox/default-placement action.
- Client navigation state may recover by refreshing organization data; I1 does not define Increment 6 offline merge/conflict semantics.

## 10. Trace mapping

| Requirement | Navigation interpretation in this model |
|---|---|
| `SRS-ORG-001` | Canonical hierarchy is Folder → List → Column; Folder may be absent from the visible ancestry of a List. |
| `SRS-ORG-002` | Inbox is the default destination when Task/Event creation has no explicit placement; I1 applies this to Basic Task. |
| `SRS-ORG-003` | Every List has a default Column used when no explicit Column is chosen. |
| `SRS-ORG-004` | The sole default Column may be hidden; `not_sectioned` is not required user-facing navigation. |
| `SRS-ORG-005` | `Tab` and `Section` are not separate navigation/domain entities from Column. |
| `SRS-ORG-006` | Full main-navigation presentation is explicitly deferred to Increment 5; this I1 model supplies the domain/navigation semantics it will present. |
| `SRS-NFR-SEC-003` | Private organization discovery and identifier resolution are owner-scoped and reject cross-user access. |

## 11. Acceptance-oriented scenarios

Implementation/test design derived from this model should include at least these scenarios:

| Area | Required scenario |
|---|---|
| Bootstrap | Authenticated User has an Inbox/default Column available before ordinary organization is created. |
| Folder optionality | User can navigate/use a Folderless List without a visible synthetic Folder. |
| Default Column | New/selected List resolves omitted Column placement to its default Column. |
| Hidden default | Sole default Column can be absent from user-facing navigation while Task placement remains concrete. |
| Multiple Columns | Explicit owned Column is selectable only under its owning List. |
| Inbox fallback | Global Task create with no destination lands in Inbox/default Column. |
| Foreign IDs | Another User's Folder/List/Column cannot be discovered, navigated, or used as Task destination. |
| Relationship validation | Column/List mismatch is rejected server-side. |
| Legacy terms | No separate Tab or Section entity/navigation level is introduced. |
| Scope guard | I1 analysis does not prescribe List/Kanban/Timeline, Calendar, final main-navigation chrome, Group navigation, or offline sync semantics. |

## 12. Design handoff constraints

Implementation and later UI design following this analysis must preserve these boundaries:

- Folder is optional in the user experience; List/Column placement is not.
- Inbox is a special default destination and must resolve to concrete owned placement.
- Every List has a default Column.
- A sole default Column may be visually hidden without weakening the underlying placement invariant.
- `Tab`, `Section`, and `not_sectioned` must not become additional user-facing domain levels.
- Server-side navigation/resource lookup and destination validation are owner-scoped.
- I1 remains personal-only for Folder/List/Column ownership; Group/shared navigation waits for Increment 7.
- Final navigation layout and alternate views remain presentation work for Increment 5 and must not redefine the organization hierarchy.
