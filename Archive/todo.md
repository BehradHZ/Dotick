# System Architecture & Technical Specification

## Project: Next-Gen Task, Routine & Event Management Platform

## 1. Executive Summary & Core Objectives

### 1.1 Vision

An enterprise-grade, modular, offline-first productivity platform combining **Tasks**, **Incremental Habit Routines**, and **Calendar Events** into a unified workspace.

### 1.2 Core Goals

* **Personal & Enterprise Workspace:** Function as a daily personal driver while maintaining strict modular software design suitable for enterprise team/organization management.
* **Portfolio Standards:** Adhere to clean code practices, strict software engineering principles, robust data normalization, and scalable design patterns.

### 1.3 Multi-Platform Phased Delivery
* **Phase 1:** Cross-platform Web Application (desktop and mobile web) built using React / React Native for Web with Google OAuth 2.0 authentication.
* **Phase 2:** Native desktop and mobile applications utilizing platform-specific UI rendering engines, background threads, native animations, and OS-level optimizations.

---

## 2. Class Table Inheritance (CTI) Database Architecture

The core domain model uses **Class Table Inheritance (CTI)** in PostgreSQL to maintain absolute normalization while preserving object-oriented inheritance.

```
                           +------------------------+
                           |      base_events       | (Parent Table)
                           +------------------------+
                           | id (PK, UUID)          |
                           | title (VARCHAR)        |
                           | description (TEXT/MD)  |
                           | start_time (TIMESTAMPTZ|
                           | end_time (TIMESTAMPTZ) |
                           | recurrence_rule (JSON) |
                           | reminders (JSONB)      |
                           | attachments (JSONB)    |
                           | created_at, updated_at |
                           +------------------------+
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

| Attribute / Feature | Base Event | Task | Routine |
| --- | --- | --- | --- |
| **Primary Identifier** | `id` (UUID) | `event_id` (FK to `base_events.id`) | `event_id` (FK to `base_events.id`) |
| **Title & Description** | Rich Markdown | Inherited | Inherited |
| **Event Horizon** | `start_time` & `end_time` | Inherited from `base_events` | Inherited from `base_events` |
| **Appears in Lists & Folders** | Yes (alongside Tasks) | Yes | No (isolated in Routine Section) |
| **Due Date & Time** | N/A | Supported (Independent roll-over) | N/A |
| **Deadline Date & Time** | N/A | Supported (Hard cutoff) | N/A |
| **Actionable / Checkable** | No | Yes (`TODO`, `DONE`, `OVERDUE`, `WONT_DO`, `AUTO_WONT_DO`) | Yes (Logged via `routine_logs`) |
| **Subtask Tree** | No | Supported (`parent_task_id`) | No |
| **Streak & Target System** | No | No | Supported (`target_unit`, `step_value`) |

---

## 3. Subtask Architecture, Cascading Rules & Cycle Prevention

### 3.1 Tree Structure

* **Inheritance & Hierarchy:** Subtasks are full `Task` entities inheriting folder, list, and tab contextual properties from the root parent.
* **Tree Depth:** Infinite depth supported at the database layer; UI visual indentation bounded to 5-6 levels to preserve layout clarity on mobile displays.

### 3.2 Cyclic Dependency Protection (DAG Validation)

Before updating `parent_task_id`, the system enforces a Directed Acyclic Graph (DAG) validation check to prevent infinite parent-child loops:

$$\text{ParentCandidate} \notin \text{Descendants}(\text{Task}_{\text{id}}) \quad \land \quad \text{ParentCandidate} \neq \text{Task}_{\text{id}}$$

* **Enforcement:** If a user attempts to set a task's parent to itself or to any of its direct or indirect child subtasks, the API rejects the transaction with a `422 Unprocessable Entity (Circular Dependency Detected)` error.

### 3.3 Cascading Deadline Mechanics

$$\text{Deadline}_{\text{subtask}} \le \text{Deadline}_{\text{parent}}$$

1. **Parent Deadline Moved Earlier:**
   * Automatically shifts all subtask deadlines earlier to match or precede the parent's new deadline.

2. **Parent Deadline Moved Later:**
   * Handled based on user setting:
     * **Option A (Default):** Shift all subtask deadlines forward proportionally.
     * **Option B:** Keep subtask deadlines unchanged.
     * **Option C (Interactive Prompt):** Trigger a scrollable modal displaying all subtasks with selection check-boxes for explicit batch adjustment.

3. **Parent Due Date Shift:**

$$\text{Subtask}_{\text{due\_date}} \le \text{Subtask}_{\text{deadline}} \le \text{Parent}_{\text{deadline}}$$

   * A subtask's `due_date` is structurally independent of the parent's `due_date`.
   * **Validation Rule:** A subtask's `due_date` cannot be set beyond its own `deadline`, which itself cannot exceed the parent task's `deadline`. Violating this throws a `422 Unprocessable Entity` validation error.

---

## 4. Jalali & Gregorian Recurrence Engine

### 4.1 End-of-Month Edge Case Handling

To preserve exact recurrence targets (e.g., distinguishing between 30th and 31st across varying month lengths):

$$\text{ScheduledDay}(y, m) = \min\Big(\text{TargetDay}, \text{DaysInMonth}(y, m, \text{CalendarType})\Big)$$

* **Behavioral Execution:**
  * Setting a recurrence target of `31` maps to the 31st in 31-day months, clamps to the 30th in 30-day months, clamps to 29/30 in Esfand (Persian calendar) / February (Gregorian), and automatically restores to the 31st when entering a 31-day month.
  * Setting a recurrence target of `30` remains strictly on the 30th (even during 31-day months) and only clamps down to 29 during leap-year edge cases.

---

## 5. Task Lifecycle & State Transitions

```
[ Active Task ] ───(Due Date Passes)───> [ Roll Over to Next Day ]
       │
       ├───(Deadline Passes)───────────> [ State: OVERDUE (Red Highlight) ]
       │
       ├───(Inactivity Threshold)──────> [ State: AUTO_WONT_DO ]
       │                                            │
       │                                            ▼
       │                                 [ Moved to Review Log ]
       │
       └───(User Clicks Postpone)─────>  [ Due Date & Deadline Reset to Today ]

```

### 5.1 Synchronization, Conflict Resolution & Real-Time Sync

```
[ Client A (Mobile) ] ──(Field Patch Delta)──> [ API Gateway ]
                                                     │
                                           (Field-Level LWW Merge)
                                                     │
[ Client B (Desktop) ] <───(WebSocket/SSE)─── [ Postgres DB ]

```

### 5.2 Auto Wont-Do Mechanics

* **Trigger:** Uncompleted tasks exceeding an inactivity threshold (e.g., 3 to 7 days).
* **Impact:**
  * Automatically marked as `AUTO_WONT_DO`.
  * Negatively impacts completion statistics.
  * Extracted from active daily views and staged into a dedicated **Auto Wont-Did Review View**.
* **Review Lifecycle:** Tasks remain in the review list until acknowledged or modified by the user.

### 5.3 Field-Level Last-Write-Wins (LWW)

1. **Delta Patch Format:** Clients emit mutations specifying dirty fields along with client UTC timestamps:

```json
{
  "entity_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "entity_type": "TASK",
  "field_updates": {
    "title": {"value": "Updated Title", "timestamp": "2026-07-30T21:15:00Z"},
    "status": {"value": "DONE", "timestamp": "2026-07-30T21:18:00Z"}
  }
}
```

2. **Resolution Strategy:** The server compares the payload's field-level `timestamp` against the existing field state. The newest timestamp wins per field.
3. **Real-time Broadcast:** Upon successful database merge, the backend broadcasts a lightweight event via WebSocket/SSE to all authenticated client sessions to trigger UI reconciliation.

---

## 6. Incremental Routines & Metrics Engine

### 6.1 Habit Data Model

Routines decouple habit definitions from daily execution state:

* **Table: `routines`** (Defines unit type, initial target, and increment step value).
* **Table: `routine_logs`**
  * `id` (PK, UUID)
  * `routine_id` (FK to `routines.event_id`)
  * `logged_date` (DATE)
  * `target_value` (NUMERIC)
  * `achieved_value` (NUMERIC)
  * `status` (ENUM: `DONE`, `FAILED`)
  * `notes` (TEXT)

### 6.2 Target Escalation Algorithm

$$\text{Target}_{t} =  \begin{cases}  \text{Target}_{t-1} + \text{StepValue}, & \text{if State}_{t-1} = \text{DONE} \\ \text{Target}_{t-1}, & \text{if State}_{t-1} = \text{FAILED} \end{cases}$$

### 6.3 Routine Schema & Streak Logic

* **Data Decomposition:**
  * `Routine`: Stores definitions, unit identifiers, initial values, and step offsets.
  * `RoutineLog`: Stores execution entries per date, targets reached, status (`DONE`/`FAILED`), and qualitative notes.
* **Streak Calculation:** Missing a single routine day instantly resets the `Streak Counter` to `0`, even if the target value remains unchanged for subsequent attempts.

---

## 7. Organizational Hierarchy & Kanban Modes

```
[ Folder ]
   └── [ List ]
        └── [ Kanban Tab ]
             └── [ Task / Event ]

```

### 7.1 Default State & Dual Kanban Modes

* Every list contains an unsectioned default tab (`NOT_SECTIONED`), hidden unless additional tabs are added.
* **Operating Modes:**
  1. **Status Mode:** Columns bind directly to the task `status` attribute (e.g., `TODO`, `IN_PROGRESS`, `DONE`).
  2. **Custom Mode:** Columns bind to `kanban_tab_id`, serving strictly as visual categorization boards without changing execution status.

---

## 8. Data Synchronization & Offline Architecture

### 8.1 Field-Level Delta Patching (Anti-Data Loss Protocol)

To prevent data overwrite bugs inherent to naive **Last-Write-Wins (LWW)** object replacement, the synchronization engine utilizes field-level mutations:

```json
{
  "entity_id": "task_8f92a10",
  "client_timestamp": "2026-07-30T10:15:00Z",
  "dirty_fields": {
    "title": "Updated Engine Architecture",
    "status": "IN_PROGRESS"
  }
}
```

* **Merge Strategy:** Server receives operational deltas, applies mutations at the attribute field layer, and resolves concurrent field-level conflicts using timestamp resolution or explicit conflict state flags.

### 8.2 Client Reconnection Sync Order

When a client transitions from offline to online, synchronization follows a strict **Push-First, Pull-Second** sequence:

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

1. **Phase 1 (Push Offline Deltas):** The client sends all queued local field-level changes (`dirty_fields`) to the backend.
2. **Phase 2 (Server Conflict Resolution):** The server merges client deltas into the database using Field-Level Last-Write-Wins (LWW).
3. **Phase 3 (Pull & Reconcile):** The client fetches updated state deltas from the server to synchronize its local cache and update the UI.

### 8.3 Local Edits vs. Server Auto-WONT_DO Resolution

* **Rule of Intent:** Explicit user action overrides automated background operations.
* **Conflict Scenario:** If the server marked an inactive task as `AUTO_WONT_DO` while a client was offline, but the offline client explicitly modified or completed that task during the offline period:
  * The server prioritizes the client's explicit field mutation.
  * The `AUTO_WONT_DO` state is invalidated and replaced by the client's updated status (e.g., `DONE` or `IN_PROGRESS`).

---

## 9. High-Performance Temporal Indexing (Inverted Date Index)

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

## 10. External LLM Natural Language Pipelines (Voice & Email)

All unstructured inputs are processed via an **external LLM service** (e.g., GPT-4o / Claude API) returning strict JSON operational schemas.

```
[ Audio Input ] ──> [ STT Engine ] ──> [ Raw Text ] ──┐
                                                      ├──> [ External LLM API ] ──> [ Structured Entity JSON ]
[ Email Inbound ] ──> [ Forwarding Hook ] ───────────┘

```

### 10.1 Semantic Actionability Disambiguation

The LLM distinguishes between **Tasks** and **Events** based on functional intent:

* **Task Intent:** Semantic presence of an actionable completion objective.
  * *Example:* "Remind me to finish the project report by tomorrow." $\rightarrow$ `{ "entity": "TASK", "action": "CREATE" }`

* **Event Intent:** Semantic presence of a time-bound attendance or calendar commitment without direct check-off completion.
  * *Example:* "Remind me to attend the Database Systems lecture on Saturday at 8 AM." $\rightarrow$ `{ "entity": "EVENT", "action": "CREATE" }`

### 10.2 Enterprise Email Forwarding Ingestion

* All inbound academic/enterprise emails are forwarded directly to a dedicated webhook pipeline (`ingest@app.domain.com`).
* The payload is sanitized and parsed by the LLM to extract dates, assignments, or exam events, automatically staging them into the user's default inbox list.

---

## 11. Next Implementation Roadmap & Integrations

1. **NLP & Voice Processing Service:** Parsing voice memos into context-aware tasks, routine items, or calendar events mapped to specific folders and tags.
2. **Enterprise Email Integration:** Parsing academic/enterprise inbound emails (e.g., university portals) to automatically schedule coursework deadlines and events.
3. **Coaching & Social Collaboration Workspace:** Granular sharing of folders, lists, and routines for remote training, student coaching, and peer accountability.
4. **Custom Metric Tracking:** Defining secondary tracking parameters (e.g., wait times, mood ratings, energy expenditure) per task execution.

---

## 12. Active Design Challenges Under Review

The following architectural challenges are currently being evaluated:

1. **Database Inheritance Strategy:** Choosing between **Single Table Inheritance (STI)** for query speed vs. **Class Table Inheritance (CTI)** for strict schema normalization across `Event`, `Task`, and `Routine`.
2. **Auto Wont-Do Worker Evaluation:** Selecting between **Lazy Evaluation** on client query vs. **Eager Asynchronous Cron Workers** on free-tier infrastructure.

---