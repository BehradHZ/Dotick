from django.urls import path

from dotick.identity import api

urlpatterns = [
    path("account", api.AccountDetail.as_view()),
    path("account/contacts", api.AccountContacts.as_view()),
    path("account/contacts/verify", api.VerifyAccountContact.as_view()),
    path("account/contacts/<uuid:contact_id>", api.DeleteAccountContact.as_view()),
]
