from django.urls import path

from dotick.identity import api

urlpatterns = [
    path("contacts", api.AccountContacts.as_view()),
    path("contacts/verify", api.VerifyAccountContact.as_view()),
    path("contacts/<uuid:contact_id>", api.DeleteAccountContact.as_view()),
]
