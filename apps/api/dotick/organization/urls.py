from django.urls import path

from dotick.organization import api

urlpatterns = [
    path("folders", api.Folders.as_view()),
    path("folders/<uuid:folder_id>", api.FolderDetail.as_view()),
]
