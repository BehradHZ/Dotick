from django.urls import path
from dotick.foundation.api import CheckpointDetail, CheckpointList

from config.operations import health, ready

handler400 = "config.errors.bad_request"
handler404 = "config.errors.not_found"
handler500 = "config.errors.server_error"

urlpatterns = [
    path("health", health),
    path("ready", ready),
    path("api/v1/foundation/checkpoints", CheckpointList.as_view()),
    path("api/v1/foundation/checkpoints/<uuid:checkpoint_id>", CheckpointDetail.as_view()),
]
