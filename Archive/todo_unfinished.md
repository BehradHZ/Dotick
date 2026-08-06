# System Architecture & Technical Specification

## Project: Next-Gen Task, Routine & Event Management Platform

---

## 1. Executive Summary & Core Objectives

### 1.1 Vision

An enterprise-grade, modular, offline-first productivity platform combining **Tasks**, **Incremental Habit Routines**, and **Calendar Events** into a unified system.

### 1.2 Multi-Platform Phased Delivery

* **Phase 1:** Cross-platform Web Application (desktop and mobile web) built using React / React Native for Web with Google OAuth 2.0 authentication.
* **Phase 2:** Native desktop and mobile applications utilizing platform-specific UI rendering engines, native threads, and OS-level optimizations.

---

## 2. Class Table Inheritance (CTI) Database Architecture

The core domain model uses **Class Table Inheritance (CTI)** in PostgreSQL to maintain normalization while supporting distinct behavioral entities.

```
                           +-------------------------+
                           |      base_events        | (Parent Table)
                           +-------------------------+
                           | id (PK, UUID)           |
                           | title (VARCHAR)         |
                           | description (TEXT/MD)   |
                           | start_time (TIMESTAMPTZ)|
                           | end_time (TIMESTAMPTZ)  |
                           | recurrence_rule (JSON)  |
                           | reminders (JSONB)       |
                           | attachments (JSONB)     |
                           | created_at, updated_at  |
                           +-------------------------+
                                      |
                 +--------------------+--------------------+
                 |                                         |
                 v                                         v
    +-------------------------+               +-------------------------+
    |          tasks          | (Child Table) |        routines         | (Child Table)
    +-------------------------+               +-------------------------+
    | event_id (PK, FK)       |               | event_id (PK, FK)       |
    | due_date (TIMESTAMPTZ)  |               | target_unit (VARCHAR)   |
    | deadline (TIMESTAMPTZ)  |               | initial_target (NUMERIC)|
    | status (ENUM)           |               | step_value (NUMERIC)    |
    | parent_task_id (FK, UUID|               | current_target (NUMERIC)|
    | kanban_tab_id (FK, UUID)|               | streak_count (INT)      |
    +-------------------------+               +-------------------------+

```

### 2.1 Entity Attribute & Organizational Matrix

| Attribute / View Context | Base Event | Task | Routine |
| --- | --- | --- | --- |
| **Primary Key** | `id` (UUID) | `event_id` (FK to `base_events.id`) | `event_id` (FK to `base_events.id`) |
| **Appears in Lists & Folders** | **Yes** (Alongside Tasks) | **Yes** | **No** (Isolated in Routine Section) |
| **Actionable Status** | Read-Only Event | `TODO`, `DONE`, `OVERDUE`, `WONT_DO`, `AUTO_WONT_DO` | Executed via `routine_logs` |
| **Due / Deadline Support** | `start_time` & `end_time` | Independent `due_date` & `deadline` | Scheduled Habit Window |
| **Subtask Tree Support** | No | **Yes** (`parent_task_id`) | No |

---

## 3. Subtask Architecture & Cycle Prevention Mechanics

### 3.1 Depth Limits & Hierarchy

* **UI Indentation Limit:** Visual nesting in the user interface is strictly capped at **5 levels** of visual offset to preserve layout usability on mobile screens.
* **Database Support:** Unbounded hierarchical depth supported at the relational storage layer.

### 3.2 Cyclic Dependency Protection (DAG Validation)

Before updating `parent_task_id`, the system enforces a Directed Acyclic Graph (DAG) validation check to prevent infinite parent-child loops:

$$\text{ParentCandidate} \notin \text{Descendants}(\text{Task}_{\text{id}}) \quad \land \quad \text{ParentCandidate} \neq \text{Task}_{\text{id}}$$

* **Enforcement:** If a user attempts to set a task's parent to itself or to any of its direct or indirect child subtasks, the API rejects the transaction with a `422 Unprocessable Entity (Circular Dependency Detected)` error.

---

## 4. Synchronization Protocol & Auto-WONT_DO Resolution

```
                  [ Offline Client Reconnects ]
                               │
               Step 1: PUSH Local Offline Deltas
                               │
                               ▼
            [ Server Evaluates Conflicts & Timestamps ]
                               │
              Step 2: PULL Server State & Reconcile

```

### 4.1 Client Reconnection Sync Order

When a client transitions from offline to online, synchronization follows a strict **Push-First, Pull-Second** sequence:

1. **Phase 1 (Push Offline Deltas):** The client sends all queued local field-level changes (`dirty_fields`) to the backend.
2. **Phase 2 (Server Conflict Resolution):** The server merges client deltas into the database using Field-Level Last-Write-Wins (LWW).
3. **Phase 3 (Pull & Reconcile):** The client fetches updated state deltas from the server to synchronize its local cache and update the UI.

### 4.2 Local Edits vs. Server Auto-WONT_DO Resolution

* **Rule of Intent:** Explicit user action overrides automated background operations.
* **Conflict Scenario:** If the server marked an inactive task as `AUTO_WONT_DO` while a client was offline, but the offline client explicitly modified or completed that task during the offline period:
* The server prioritizes the client's explicit field mutation.
* The `AUTO_WONT_DO` state is invalidated and replaced by the client's updated status (e.g., `DONE` or `IN_PROGRESS`).



---

## 5. High-Performance Temporal Indexing (Inverted Date Index)

To avoid heavy runtime scans and repeated table joins when building temporal dashboard views (**Today**, **Tomorrow**, **This Week**, **This Month**), the backend maintains an **Inverted Temporal Bucket Index**.

```
[ Inverted Date Index ]
 ├── "bucket:today:2026-07-31"      --> [task_uuid_1, event_uuid_4, ...]
 ├── "bucket:tomorrow:2026-08-01"   --> [task_uuid_3, event_uuid_9, ...]
 └── "bucket:this_week:2026-W31"    --> [task_uuid_1, task_uuid_3, ...]

```

* **Data Structure:** Indexed lookup views / Redis key sets mapping date buckets directly to pre-filtered entity IDs (`base_event_id`).
* **Query Performance:** Reduces dashboard view rendering queries from $O(N)$ full table joins to $O(1)$ indexed lookup queries.

---

## 6. External LLM Natural Language Pipelines (Voice & Email)

All unstructured inputs are processed via an **external LLM service** (e.g., GPT-4o / Claude API) returning strict JSON operational schemas.

```
[ Audio Input ] ──> [ STT Engine ] ──> [ Raw Text ] ──┐
                                                      ├──> [ External LLM API ] ──> [ Structured Entity JSON ]
[ Email Inbound ] ──> [ Forwarding Hook ] ───────────┘

```

### 6.1 Semantic Actionability Disambiguation

The LLM distinguishes between **Tasks** and **Events** based on functional intent:

* **Task Intent:** Semantic presence of an actionable completion objective.
* *Example:* "Remind me to finish the project report by tomorrow." $\rightarrow$ `{ "entity": "TASK", "action": "CREATE" }`


* **Event Intent:** Semantic presence of a time-bound attendance or calendar commitment without direct check-off completion.
* *Example:* "Remind me to attend the Database Systems lecture on Saturday at 8 AM." $\rightarrow$ `{ "entity": "EVENT", "action": "CREATE" }`



### 6.2 Enterprise Email Forwarding Ingestion

* All inbound academic/enterprise emails are forwarded directly to a dedicated webhook pipeline (`ingest@app.domain.com`).
* The payload is sanitized and parsed by the LLM to extract dates, assignments, or exam events, automatically staging them into the user's default inbox list.

---

## 7. Jalali & Gregorian Recurrence Clamping Formula

$$\text{ScheduledDay}(y, m) = \min\Big(\text{TargetDay}, \text{DaysInMonth}(y, m, \text{CalendarType})\Big)$$

* **TargetDay = 31:** Evaluates to 31 in 31-day months, clamps to 30 in 30-day months, clamps to 29/30 in Esfand / February, and automatically restores to 31 when entering a 31-day month.

---