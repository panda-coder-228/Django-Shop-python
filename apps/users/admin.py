from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomerUser


@admin.register(CustomerUser)
class CustomerUserAdmin(UserAdmin):

    list_display = (
        "avatar",
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_display_links = (
        "email",
    )


    fieldsets = (
        ("Основная информация", {
            "fields": (
                "email",
                "password",
            )
        }),

        ("Персональная информация", {
            "fields": (
                "first_name",
                "last_name",
                "phone",
                "avatar",
                "about",
            )
        }),

        ("Права доступа", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Даты", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )


    filter_horizontal = (
        "groups",
        "user_permissions",
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
        "groups",
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