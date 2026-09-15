from django.urls import path

from dotick.tasks import api

urlpatterns = [
    path("tasks", api.Tasks.as_view()),
    path("tasks/<uuid:task_id>", api.TaskDetail.as_view()),
    path("tasks/<uuid:task_id>/restore", api.TaskRestore.as_view()),
]
