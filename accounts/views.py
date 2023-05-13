from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, UpdateView
from django.views.generic.edit import CreateView
from django.views import View

from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .models import *
from .forms import *

from django.urls import reverse_lazy as _


# Signu, Login and Logout View
# SIGN-UP 
class SignupView(CreateView):
    form_class = SignupForm
    success_url = _("login")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        # Save the form data to the database
        response = super().form_valid(form)
        form.save()
        messages.success(self.request, "Account Created")
        return response
# LOGIN => Its a Funcation base view case Class base view not working ASK SIR ABOUT THIS
def login_user(request):
    form = LoginForm
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, email=email.lower(), password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Either Username or Password Doesn't Matched")
            return redirect("login")

    return render(request, "accounts/login.html", {"form": form})
# LOG-OUT
class LogoutView(LogoutView):
    next_page = _("login")


# User Profile View
# PROFILE VIEW
class ProfileView(LoginRequiredMixin, View):
    template_name = "accounts/profile_view.html"

    def get(self, request, *args, **kwargs):
        profiles = Profile.objects.filter(profile=request.user)
        context = {"profiles": profiles}
        return render(self.request, self.template_name, context)

# CRUD Operation for User Profile
# CREATE
class ProfileAdd(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile_form.html"
    success_url = _("profile-view")

    def form_valid(self, form):
        try:
            profile = Profile.objects.get(profile=self.request.user)
            messages.info(self.request, "You already have a profile. Please update it to make any changes")
            return redirect('profile-view')
        except Profile.DoesNotExist:
            profile = form.save(commit=False)
            profile.profile = self.request.user
            profile.save()
            messages.success(self.request, "Your New Profile Has Been Created Successfully")
            return super().form_valid(form)
# UPDATE
class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "accounts/profile_form.html"
    success_url = _("profile-view")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your Profile Has Been Updated Successfully")
        return response

    



# class LoginView(View):
#     form = LoginForm
#     template_name = 'accounts/login.html'

#     def get(self, request):
#         form = self.form()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = self.form(request.POST)
#         if form.is_valid():

#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']

#             user = authenticate(request, email=email.lower(), password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 messages.error(request, "Please Check Your Email ID or Password")
#                 return redirect('login')
#         return render(request, self.template_name, {"form": form})