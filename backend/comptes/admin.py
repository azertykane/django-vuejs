from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Utilisateur

@admin.register(Utilisateur)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "role", "is_staff")
    fieldsets = (
        (None,               {"fields": ("email", "password")}),
        (_("Informations"),  {"fields": ("telephone", "cni", "role")}),
        (_("Permissions"),   {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Dates"),         {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role"),
        }),
    )
    search_fields = ("email",)
