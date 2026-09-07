from django.urls import path
from dotick.foundation.api import CheckpointDetail, CheckpointList
from dotick.identity.api import (
    Logout,
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
    path("api/v1/auth/logout", Logout.as_view()),
    path("api/v1/auth/sessions", Sessions.as_view()),
    path("api/v1/auth/sessions/<uuid:session_id>", SessionDetail.as_view()),
    path("api/v1/auth/password/reset/request", PasswordResetRequest.as_view()),
    path("api/v1/auth/password/reset/confirm", PasswordResetConfirm.as_view()),
    path("api/v1/foundation/checkpoints", CheckpointList.as_view()),
    path("api/v1/foundation/checkpoints/<uuid:checkpoint_id>", CheckpointDetail.as_view()),
]
