from django.urls import path

from dotick.identity import api

urlpatterns = [
    path("register", api.Register.as_view()),
    path("email/resend", api.ResendEmailVerification.as_view()),
    path("email/verify", api.VerifyEmail.as_view()),
    path("token", api.CreateTokenPair.as_view()),
    path("token/refresh", api.RotateRefreshToken.as_view()),
    path("logout", api.LogoutCurrentSession.as_view()),
]
