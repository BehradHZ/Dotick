from django.urls import path

from dotick.identity import api

urlpatterns = [
    path("register", api.Register.as_view()),
    path("email/resend", api.ResendEmailVerification.as_view()),
    path("email/verify", api.VerifyEmail.as_view()),
    path("password/reset/request", api.RequestPasswordReset.as_view()),
    path("password/reset/confirm", api.ConfirmPasswordReset.as_view()),
    path("password", api.SetPassword.as_view()),
    path("google", api.GoogleSignIn.as_view()),
    path("google/link", api.LinkGoogleIdentity.as_view()),
    path("passkeys/registration/options", api.BeginPasskeyRegistration.as_view()),
    path("passkeys/registration/verify", api.FinishPasskeyRegistration.as_view()),
    path("passkeys/authentication/options", api.BeginPasskeyAuthentication.as_view()),
    path("token", api.CreateTokenPair.as_view()),
    path("token/refresh", api.RotateRefreshToken.as_view()),
    path("logout", api.LogoutCurrentSession.as_view()),
    path("sessions", api.ActiveSessions.as_view()),
    path("sessions/<uuid:session_id>", api.RevokeOwnedSession.as_view()),
]
