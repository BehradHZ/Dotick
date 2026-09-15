from django.urls import path

from dotick.tasks import api

urlpatterns = [
    path("tasks", api.Tasks.as_view()),
]
