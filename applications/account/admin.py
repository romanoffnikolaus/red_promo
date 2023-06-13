from django.contrib import admin

from .models import User, Renters

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active') 
    search_fields = ['username', 'email', 'first_name', 'last_name', 'is_active']
    fields = [
        'last_login',
        'groups',
        ('username', 'email'),
        ('first_name', 'last_name'),
        ('is_active', 'is_staff', 'is_superuser'),
    ]

admin.site.register(Renters)