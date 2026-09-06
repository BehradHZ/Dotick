from django.db import transaction
from django.http import Http404

from dotick.foundation.models import Checkpoint


@transaction.atomic
def create_checkpoint(*, actor_id, text):
    return Checkpoint.objects.create(owner_id=actor_id, text=text.strip())


def list_checkpoints(*, actor_id):
    return Checkpoint.objects.filter(owner_id=actor_id)[:100]


def get_checkpoint(*, actor_id, checkpoint_id):
    try:
        return Checkpoint.objects.filter(owner_id=actor_id).get(id=checkpoint_id)
    except Checkpoint.DoesNotExist as error:
        raise Http404 from error
