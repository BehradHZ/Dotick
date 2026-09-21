import hashlib

from django.db import connection, transaction


def lock_create_operation_scope(*, actor_id, resource_type, operation_id):
    if not transaction.get_connection().in_atomic_block:
        raise RuntimeError("Create-operation locking requires an active transaction.")

    scope = f"{actor_id}:{resource_type}:{operation_id}".encode()
    lock_key = int.from_bytes(hashlib.sha256(scope).digest()[:8], byteorder="big", signed=True)
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_advisory_xact_lock(%s)", [lock_key])
