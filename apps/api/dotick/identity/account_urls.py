from django.urls import path

from dotick.identity import api

urlpatterns = [
    path("contacts", api.AccountContacts.as_view()),
]
