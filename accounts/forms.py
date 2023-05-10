from django import forms
# from django.forms import EmailField

from django.contrib.auth.forms import UserCreationForm
from .models import User

class LowerEmailField(forms.EmailField):
    def clean(self, value):
        cleaned_value = super().clean(value)
        return cleaned_value.lower()

class SignupForm(UserCreationForm):
    email = LowerEmailField(max_length=254,
                             widget=forms.EmailInput(attrs={'class': 'form-control p_input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control p_input'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control p_input'}), label='Confirm Password')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class LoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=254,
                             widget=forms.EmailInput(attrs={'class': 'form-control p_input'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control p_input'}), label='Password')

    class Meta:
        model = User
        fields = ('email', 'password')
