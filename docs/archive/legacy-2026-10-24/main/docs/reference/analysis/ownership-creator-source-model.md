# Increment 1 Ownership, Creator, and Source/Provenance Model

> **Status:** Formal analysis artifact for Increment 1; this document does not assert implementation completion.
>
> **Date:** 2026-09-11
>
> **Authority:** System Definition ownership/collaboration rules → Decision Register → `SRS-ITEM-006..008` and `SRS-NFR-SEC-003` → this analysis artifact.

## 1. Purpose

Dotick deliberately treats **ownership**, **creator**, and **source/provenance** as three independent concepts. They may happen to point to the same human/context for a simple manually-created personal Task, but they answer different questions and must not be collapsed in the domain model, API, authorization logic, or persistence model.

```text
ownership         = whose Resource is this?
creator           = who caused this Resource to be created in Dotick?
source/provenance = how/from where did this Resource enter Dotick?
```

## 2. Ownership

Ownership answers the authorization and lifecycle question:

> Which internal Dotick principal owns this Resource?

For Increment 1 private Items this is represented by `owner_user_id`.

Ownership determines the private scope used for ordinary reads and writes. It is therefore relevant to:

- authorization and isolation;
- whether a private Resource is discoverable/queryable by the current User;
- placement validation against Folder/List/Column owned by the same User;
- user-facing personal data lifecycle such as Trash/export/deletion behavior;
- future sharing/group rules when those capabilities enter their owning increment.

### I1 ownership rules

1. `owner_user_id` is server-controlled authority and is never trusted from ordinary client create/update payloads.
2. For a personal I1 Task, ownership is derived from the authenticated User at creation.
3. Private Item lookup begins inside the authenticated User's ownership scope.
4. Source/provenance must never grant ownership.
5. Creator identity must never be used as a substitute ownership check.
6. Moving a Task between owned Columns does not change ownership.
7. Ordinary title/status edits do not change ownership.

## 3. Creator

Creator answers the historical attribution question:

> Which internal Dotick User initiated the creation of this Resource?

For Items this is represented by `created_by_user_id`.

Creator is not an authorization shortcut. It records who caused the Item to exist, not who currently owns it or who may currently access it.

### I1 creator rules

1. `created_by_user_id` is derived from authenticated server context when the Item is created.
2. In I1 personal-only flows, `created_by_user_id` and `owner_user_id` normally contain the same User because users create their own private Tasks.
3. They remain separate fields because later collaboration can make creator and owner legitimately different without changing the meaning of either concept.
4. Creator is historical attribution and is not rewritten by ordinary edit, move, complete, reopen, Trash, or restore operations.
5. A matching creator does not by itself authorize access if ownership/authorization rules do not permit that access.
6. A non-matching creator must not by itself deny access to a legitimate owner or later authorized collaborator.

## 4. Source / provenance

Source answers the provenance question:

> Through what origin/channel did this Item enter Dotick?

Increment 1 uses a basic source record with:

```text
platform
external_account_id? 
external_id?
```

`manual` is a valid source platform.

Source may later identify an external integration/import origin, but it is metadata about origin, not internal ownership or authorization.

### I1 source rules

1. Source is separate from `owner_user_id` and `created_by_user_id`.
2. `platform = manual` is valid for ordinary Dotick-created Tasks.
3. `external_account_id` and `external_id` are optional provider-scoped provenance identifiers.
4. External identifiers are not Dotick User IDs and must not be interpreted as such.
5. Source must not grant read/write permission.
6. Changing or losing an external integration must not silently change internal ownership.
7. Source identity may participate in integration-level deduplication/idempotency, but never replaces the Item's stable internal UUID.

## 5. Relationship matrix

| Question | Ownership | Creator | Source / provenance |
|---|---|---|---|
| Whose Resource is it? | Yes | No | No |
| Who initiated creation in Dotick? | No | Yes | No |
| Where/how did it originate? | No | No | Yes |
| Used as primary private authorization scope? | Yes | No | No |
| Normally server-derived in I1? | Yes | Yes | Yes/basic provenance |
| May differ from ownership in later collaboration? | — | Yes | Yes |
| May grant access by itself? | Ownership participates in authorization | No | No |
| Stable historical attribution? | Current ownership concept | Yes | Yes |

## 6. I1 examples

### Example A — Manual personal Task

```text
owner_user_id      = User A
created_by_user_id = User A
source.platform    = manual
```

The values coincide, but their meanings do not.

### Example B — Future imported Item

Conceptually, a future integration could produce:

```text
owner_user_id               = User A
created_by_user_id          = User A or the authenticated importing actor
source.platform             = external_provider
source.external_account_id  = provider account reference
source.external_id          = provider object reference
```

The external account/object references do not become the Dotick owner.

### Example C — Future collaboration

A later collaboration flow may legitimately allow:

```text
owner = User/Group context A
creator = User B
source = manual
```

This is why creator and owner must not be collapsed even though I1 personal creation usually makes them equal.

## 7. Security invariants

- Never accept authoritative `owner_user_id` or `created_by_user_id` from an ordinary Task create/edit client payload.
- Never authorize a request because `created_by_user_id == actor.id` without checking the owning authorization scope.
- Never authorize a request because Source matches an external account controlled by the caller.
- Destination Folder/List/Column ownership must be validated independently from Item provenance.
- Cross-user inaccessible Resources should use the normal non-disclosing not-found/authorization-safe surface.

## 8. Persistence/API handoff

The I1 physical model should preserve these concepts independently:

```text
items.owner_user_id       -> users.id
items.created_by_user_id  -> users.id
item_sources.item_id      -> items.id
item_sources.platform
item_sources.external_account_id?
item_sources.external_id?
```

The server derives owner/creator from authenticated context for I1 creation. API response models may expose provenance as appropriate, but accepting provenance fields must never make them authoritative for ownership.

## 9. Trace

- `SRS-ITEM-006`: owner and creator are independent concepts.
- `SRS-ITEM-007`: provenance is separate from ownership; Source does not determine internal owner.
- `SRS-ITEM-008`: Task/Event Source carries platform and optional external account/external ID.
- `SRS-NFR-SEC-003`: private user data must reject cross-user access.
