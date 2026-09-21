from django.urls import path

from dotick.identity import api
from dotick.organization import api as organization_api

urlpatterns = [
    path("account", api.AccountDetail.as_view()),
    path("account/bootstrap", organization_api.AccountBootstrap.as_view()),
    path("account/contacts", api.AccountContacts.as_view()),
    path("account/contacts/verify", api.VerifyAccountContact.as_view()),
    path("account/contacts/<uuid:contact_id>", api.DeleteAccountContact.as_view()),
]
