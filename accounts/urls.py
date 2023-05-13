from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import *
from django.urls import reverse_lazy as _

urlpatterns = [
    # Signup, Login and Logout
    path("", views.SignupView.as_view(), name="signup"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("login/", views.login_user, name="login"),
    # path("login/", views.LoginView.as_view(), name='login'),

    # CRUD Operation for Profile
    path("profile-add/", views.ProfileAdd.as_view(), name="profile-add"),
    path("profile-update/<int:pk>/", views.ProfileUpdate.as_view(), name="profile-update"),
    path("profile-view/", views.ProfileView.as_view(), name="profile-view"),
    
    # Django's Default/built-in Password Reset Views 
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset/password_reset_form.html",
            email_template_name="accounts/password_reset/password_reset_email.html",
            subject_template_name="accounts/password_reset/password_reset_subject.txt",
            success_url=_("password_reset_done"),
            form_class=MyPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset/password_reset_confirm.html",
            form_class=MySetPasswordForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
