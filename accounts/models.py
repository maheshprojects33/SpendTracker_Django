from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser Must have is_staff=True")
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=40)
    email_token = models.CharField(max_length=255, blank=True)
    forget_password = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    last_logout = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    GENDER_CHOICE = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    profile_pic = models.ImageField(upload_to='profile/', blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICE, default='male')
    mobile = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)