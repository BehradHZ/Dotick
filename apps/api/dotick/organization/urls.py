from django.urls import path

from dotick.organization import api

urlpatterns = [
    path("folders", api.Folders.as_view()),
    path("folders/<uuid:folder_id>", api.FolderDetail.as_view()),
    path("folders/<uuid:folder_id>/restore", api.FolderRestore.as_view()),
    path("trash/folders", api.TrashedFolders.as_view()),
    path("lists", api.Lists.as_view()),
    path("lists/<uuid:list_id>", api.ListDetail.as_view()),
]
