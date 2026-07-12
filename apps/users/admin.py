from django.contrib import admin
from apps.users.models import CustomerUser


@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ("avatar","email", "first_name", "last_name", "phone", "about", "is_staff", "is_active", "date_joined")
    list_display_links = (
        "email",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "date_joined",
    )

    ordering = (
        "-date_joined",
    )

    readonly_fields = (
        "date_joined",
        "last_login",
    )

    list_per_page = 25