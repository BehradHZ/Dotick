# Dotick — Development Roadmap

## Overview

This roadmap outlines the development plan for Dotick, a personal productivity application, using an incremental development approach. Rather than designing the entire system in advance, the project will be built in a series of stages. Each stage adds one meaningful capability, is used in daily practice before the next stage begins, and is documented with a short written record explaining the reasoning behind the decisions made.

This approach was chosen deliberately. The developer is working alone, with a limited number of hours available each week, and with no fixed deadline. Under these conditions, an approach that assumes all requirements are known in advance is not realistic, since new ideas and needs continue to emerge over time. A staged approach allows the project to remain useful throughout its development, rather than only becoming useful once it is entirely finished.

## Guiding Principles

* Each stage must result in something that can actually be used, not just planned.
* Each stage must be reasonably complete and stable before the next one begins.
* Each stage should include a short written explanation of the key decisions made and why alternatives were not chosen.
* Complexity should be added gradually. Features that are not yet needed should be postponed rather than built in advance.
* Priority is given to the quality and clarity of the underlying structure over the number of features present at any given time.

## Stage 1 — Basic Foundation

The first stage establishes the minimum working environment for the application, including user sign-in and a working connection between the application and its underlying storage. No user-facing features are built yet. The goal is to confirm that the basic technical foundation is functioning correctly before anything is built on top of it.

## Stage 2 — Core Task Management

The second stage introduces the first real feature: the ability to create, view, edit, and complete simple tasks. This stage also establishes the underlying data structure that later stages will build upon, since tasks, routines, and calendar items will eventually share a common foundation. Getting this structure right early, even in a simplified form, is treated as a priority.

## Stage 3 — Organization and Board View

The third stage introduces a way to organize tasks visually, similar to a board with columns representing different stages of progress. This includes basic grouping of tasks into categories. Only the simplest version of this organizational system is built at this stage.

## Stage 4 — Subtasks and Structure

The fourth stage allows tasks to be broken down into smaller subtasks. Because this introduces the possibility of accidentally creating circular relationships between tasks, a safeguard is built to prevent this from happening. Rules about how deadlines are inherited between a task and its subtasks are also introduced, though only in their simplest form at first.

## Stage 5 — Task Lifecycle Management

The fifth stage introduces automatic handling of tasks that are left incomplete for too long. Such tasks are automatically flagged and moved into a separate review area rather than cluttering the main view. This stage also introduces the ability to postpone a task easily.

## Stage 6 — Habit and Routine Tracking

The sixth stage introduces a separate system for tracking recurring habits and routines, distinct from one-time tasks. This includes tracking streaks of consistency and gradually increasing targets over time as habits are maintained successfully.

## Stage 7 — Calendar Recurrence Logic

The seventh stage introduces the logic needed to handle recurring events and tasks correctly across calendars with months of different lengths, including both the Gregorian and Persian calendar systems. Particular attention is given to edge cases, such as what happens when a recurring date falls near the end of a month.

## Stage 8 — Basic Synchronization

The eighth stage introduces the ability to use the application across multiple devices, with changes made on one device properly reflected on another. At this stage, synchronization happens when the application is actively checked, rather than instantly.

## Stage 9 — Real-Time Synchronization

The ninth stage upgrades the synchronization system introduced in the previous stage so that changes appear across devices immediately, without needing to manually refresh or reopen the application. This stage is treated as optional and may be skipped if the application is only ever used by one person on one device at a time.

## Stage 10 — Performance Improvements

The tenth stage focuses on improving the speed of the application once enough real data exists to make performance noticeable. This stage is intentionally placed late in the roadmap, since performance work is most meaningful once there is real usage to measure and improve against.

## Stage 11 — Intelligent Input Processing

The eleventh and final planned stage introduces the ability to create tasks and events automatically from natural input, such as forwarded emails or spoken reminders, using an external language-understanding service. This is placed last because it depends on all of the underlying structures built in the earlier stages.

## Deliberately Postponed Items

Some capabilities described in the original planning document are intentionally left out of this roadmap for now. These include collaborative and social features intended for multiple users, more advanced organizational customization beyond the basic board view, more complex deadline inheritance rules beyond the simplest option, and native mobile and desktop applications. These are not rejected outright, but are postponed until there is a clear, demonstrated need for them based on real usage of the simpler version.

## Rule for Progression

No new stage should begin until the previous stage has been used in practice for a meaningful period of time, its key decisions have been documented, and at least one lesson learned from real use has informed the plan for what comes next. If a new stage begins without any of these being true, it is a sign that the roadmap is being followed mechanically rather than being genuinely learned from.
