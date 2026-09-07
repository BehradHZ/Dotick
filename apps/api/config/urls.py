from django.urls import path
from dotick.foundation.api import CheckpointDetail, CheckpointList
from dotick.identity.api import (
    Account,
    ContactDetail,
    Contacts,
    ContactVerify,
    GoogleLink,
    GoogleSignIn,
    Logout,
    PasskeyAuthenticationOptions,
    PasskeyAuthenticationVerify,
    PasskeyDetail,
    PasskeyRegistrationOptions,
    PasskeyRegistrationVerify,
    Passkeys,
    Password,
    PasswordResetConfirm,
    PasswordResetRequest,
    Refresh,
    Register,
    ResendEmailVerification,
    SessionDetail,
    Sessions,
    Token,
    VerifyEmail,
)
from dotick.organization.api import (
    AccountBootstrap,
    ColumnDetail,
    Columns,
    FolderDetail,
    FolderRestore,
    Folders,
    ListDetail,
    ListRestore,
    Lists,
    TrashFolders,
    TrashLists,
)
from dotick.tasks.api import TaskDetail, TaskList, TaskRestore, TrashTasks

from config.operations import health, ready

handler400 = "config.errors.bad_request"
handler404 = "config.errors.not_found"
handler500 = "config.errors.server_error"

urlpatterns = [
    path("health", health),
    path("ready", ready),
    path("api/v1/auth/register", Register.as_view()),
    path("api/v1/auth/email/verify", VerifyEmail.as_view()),
    path("api/v1/auth/email/resend", ResendEmailVerification.as_view()),
    path("api/v1/auth/token", Token.as_view()),
    path("api/v1/auth/token/refresh", Refresh.as_view()),
    path("api/v1/auth/password", Password.as_view()),
    path("api/v1/auth/google", GoogleSignIn.as_view()),
    path("api/v1/auth/google/link", GoogleLink.as_view()),
    path("api/v1/auth/passkeys", Passkeys.as_view()),
    path("api/v1/auth/passkeys/<uuid:passkey_id>", PasskeyDetail.as_view()),
    path(
        "api/v1/auth/passkeys/registration/options",
        PasskeyRegistrationOptions.as_view(),
    ),
    path(
        "api/v1/auth/passkeys/registration/verify",
        PasskeyRegistrationVerify.as_view(),
    ),
    path(
        "api/v1/auth/passkeys/authentication/options",
        PasskeyAuthenticationOptions.as_view(),
    ),
    path(
        "api/v1/auth/passkeys/authentication/verify",
        PasskeyAuthenticationVerify.as_view(),
    ),
    path("api/v1/auth/logout", Logout.as_view()),
    path("api/v1/auth/sessions", Sessions.as_view()),
    path("api/v1/auth/sessions/<uuid:session_id>", SessionDetail.as_view()),
    path("api/v1/auth/password/reset/request", PasswordResetRequest.as_view()),
    path("api/v1/auth/password/reset/confirm", PasswordResetConfirm.as_view()),
    path("api/v1/account/bootstrap", AccountBootstrap.as_view()),
    path("api/v1/account", Account.as_view()),
    path("api/v1/account/contacts", Contacts.as_view()),
    path("api/v1/account/contacts/verify", ContactVerify.as_view()),
    path("api/v1/account/contacts/<uuid:contact_id>", ContactDetail.as_view()),
    path("api/v1/folders", Folders.as_view()),
    path("api/v1/folders/<uuid:folder_id>", FolderDetail.as_view()),
    path("api/v1/folders/<uuid:folder_id>/restore", FolderRestore.as_view()),
    path("api/v1/trash/folders", TrashFolders.as_view()),
    path("api/v1/lists", Lists.as_view()),
    path("api/v1/lists/<uuid:list_id>", ListDetail.as_view()),
    path("api/v1/lists/<uuid:list_id>/restore", ListRestore.as_view()),
    path("api/v1/trash/lists", TrashLists.as_view()),
    path("api/v1/lists/<uuid:list_id>/columns", Columns.as_view()),
    path("api/v1/columns/<uuid:column_id>", ColumnDetail.as_view()),
    path("api/v1/tasks", TaskList.as_view()),
    path("api/v1/tasks/<uuid:task_id>", TaskDetail.as_view()),
    path("api/v1/tasks/<uuid:task_id>/restore", TaskRestore.as_view()),
    path("api/v1/trash/tasks", TrashTasks.as_view()),
    path("api/v1/foundation/checkpoints", CheckpointList.as_view()),
    path("api/v1/foundation/checkpoints/<uuid:checkpoint_id>", CheckpointDetail.as_view()),
]
