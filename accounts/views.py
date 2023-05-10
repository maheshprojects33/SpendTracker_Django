from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .models import *
from django.contrib import messages
from django.urls import reverse_lazy as _
from django.views.generic.edit import CreateView, FormView
from django.views.generic import View
from django.contrib.auth.views import LogoutView
from .forms import *
from django.contrib.auth import authenticate, login
from .models import User

class SignupView(CreateView):
    form_class = SignupForm
    success_url = _('login')
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        # Save the form data to the database
        response = super().form_valid(form)
        form.save()
        messages.success(self.request, "Account Created")
        return response
        
    

class LoginView(View):
    form = LoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email.lower(), password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Please Check Your Email ID or Password")
                return redirect('login')
        return render(request, self.template_name, {"form": form})
    
class LogoutView(LogoutView):
    next_page = _('login')

def login_user(request):
    form = LoginForm
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, email=email.lower(), password=password)

        if user is not None:
            login(request, user) 
            return redirect('home')
        else:
            messages.info(request, "Either Username or Password Doesn't Matched")
            return redirect('login')

    return render(request, 'accounts/login.html', {"form": form})






