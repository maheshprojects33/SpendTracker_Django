from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'last_login', 'is_active', 'is_verified', 'is_staff', 'is_superuser')
    search_fields = ('email', 'full_name')
    ordering = ('-date_joined',)


admin.site.register(User, UserAdmin)



