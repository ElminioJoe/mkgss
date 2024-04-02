from django.urls import include, path, reverse_lazy
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
)

from . import views

urlpatterns = [
    # path('authentication/', include('django.contrib.auth.urls')),
    path("login/", views.UserLoginView.as_view(), name="login"),
    # Password change views
    path(
        "password_change/",
        PasswordChangeView.as_view(
            template_name="registration/password_change.html",
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_change_done",
    ),
    # Password reset views
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    # Logout view
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
]
