from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = [
        'id', 'username', 'email', 'role'
    ]

    list_filter = [
        'role'
    ]

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields':('role',)}),
    )

admin.site.register(User, CustomUserAdmin)
