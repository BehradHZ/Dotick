from django.urls import path

from dotick.foundation.api import CheckpointDetail, CheckpointList

urlpatterns = [
    path("checkpoints/", CheckpointList.as_view()),
    path("checkpoints/<uuid:checkpoint_id>/", CheckpointDetail.as_view()),
]
