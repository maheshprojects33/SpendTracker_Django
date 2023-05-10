from django.contrib import admin
from .models import *

# Register your models here.

class CashInAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'note', 'date', 'modified_at']

admin.site.register(CashIn, CashInAdmin)

class CashOutAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', "mode", 'pay_to', 'category', 'remarks', 'date', 'modified_at']
    
admin.site.register(CashOut, CashOutAdmin)
    
admin.site.register(Category)
