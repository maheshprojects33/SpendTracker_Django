from django import forms
# from django.forms import EmailField

from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm

from .models import *
from django.contrib.auth import get_user_model

class LowerEmailField(forms.EmailField):
    def clean(self, value):
        cleaned_value = super().clean(value)
        return cleaned_value.lower()

class SignupForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Full Name')
    email = LowerEmailField(max_length=254,
                             widget=forms.EmailInput(attrs={'class': 'form-control p_input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control p_input'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control p_input'}), label='Confirm Password')

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password1', 'password2')

class LoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=254,
                             widget=forms.EmailInput(attrs={'class': 'form-control p_input'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control p_input'}), label='Password')

    class Meta:
        model = User
        fields = ('email', 'password')


# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ['profile']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address"].widget.attrs.update({"class": "form-control"})
        self.fields["mobile"].widget.attrs.update({"class": "form-control"})
        self.fields["gender"].widget.attrs.update({"class": "form-control"})
        self.fields["profile_pic"].widget.attrs.update({"class": "form-control"})
    
    

class MyPasswordResetForm(PasswordResetForm):
   
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'Email'}))
    
    class Meta:
        model = get_user_model()
        fields = ['email']

class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'New password',
            'help_text': None,
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm new password',
        })
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].help_text = None