from django.urls import path
from . import views

urlpatterns = [
    path("", views.SignupView.as_view(), name='signup'),
    # path("login/", views.LoginView.as_view(), name='login'),
    path("logout/", views.LogoutView.as_view(), name='logout'),
    path("login/", views.login_user, name='login'),
]
