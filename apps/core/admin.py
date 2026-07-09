from django.contrib import admin
from apps.core.models import Banner


@admin.register(Banner)
class AdminBanner(admin.ModelAdmin):
    list_display = ('title', 'image', 'is_active',)
    list_editable = ('is_active',)
    