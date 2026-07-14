from django.contrib import admin

from .models import MainBanner


@admin.register(MainBanner)
class MainBannerAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "banner_type",
        "product",
        "is_active",
        "position",
        "created_at",
    )

    list_filter = (
        "banner_type",
        "is_active",
    )

    search_fields = (
        "title",
        "product__title",
    )

    list_editable = (
        "is_active",
        "position",
    )