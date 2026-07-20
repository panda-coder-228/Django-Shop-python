from django.contrib import admin, messages
from .models import Warehouse, Stock, StockIssue, StockReceipt
from .services import StockIssueService, StockReceiptService, WarehouseService
from django.urls import path
from django.shortcuts import render, redirect
from .forms import StockReceiptForm, StockIssueForm
from django.urls import reverse


@admin.action(description="Активувати вибрані склади")
def activate_warehouses(modeladmin, request, queryset):
    for warehouse in queryset:
        WarehouseService.activate(warehouse)

    messages.success(
        request,
        f"Активовано: {queryset.count()} складів."
    )


@admin.action(description="Деактивувати вибрані склади")
def deactivate_warehouses(modeladmin, request, queryset):
    success = 0

    for warehouse in queryset:
        try:
            WarehouseService.deactivate(warehouse)
            success += 1
        except ValueError as e:
            messages.error(request, f"{warehouse.title}: {e}")

    if success:
        messages.success(
            request,
            f"Деактивовано: {success} складів."
        )


@admin.action(description="М'яке видалення")
def soft_delete_warehouses(modeladmin, request, queryset):
    for warehouse in queryset:
        WarehouseService.delete(warehouse)

    messages.success(
        request,
        f"Позначено як видалені: {queryset.count()} складів."
    )


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    change_list_template = "admin/warehouse/warehouse/change_list.html"

    list_display = (
        "title",
        "address",
        "is_active",
        "is_deleted",
    )

    list_editable = (
        "is_active",
        "is_deleted",
    )

    list_filter = (
        "is_active",
        "is_deleted",
    )

    search_fields = (
        "title",
        "address",
    )

    actions = (
        activate_warehouses,
        deactivate_warehouses,
        soft_delete_warehouses,
    )
    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
            "receipt/",
            self.admin_site.admin_view(self.receipt_view),
            name="warehouse_receipt",
        ),
            path(
            "issue/",
            self.admin_site.admin_view(self.issue_view),
            name="warehouse_issue",
        ),
    ]

        return custom_urls + urls
    
    def receipt_view(self, request):
        form = StockReceiptForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            try:
                StockReceiptService.create(**form.cleaned_data)

                self.message_user( request,
                "Товар успішно оприбутковано.",
                level=messages.SUCCESS,)
                return redirect(reverse("admin:warehouse_warehouse_changelist"))

            except ValueError as e:
                form.add_error(None, str(e))

        context = {**self.admin_site.each_context(request),
        "title": "Оприбуткування товару",
        "form": form,
    }

        return render(
        request,
        "admin/warehouse/receipt.html",
        context,
    )

    def issue_view(self, request):
        form = StockIssueForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            try:
                StockIssueService.create(**form.cleaned_data)

                self.message_user(
                    request,
                    "Товар успішно списано.",
                    level=messages.SUCCESS,)

                return redirect("../")

            except ValueError as e:
                form.add_error(None, str(e))

        context = {
        **self.admin_site.each_context(request),
        "title": "Списання товару",
        "form": form,
    }

        return render(
        request,
        "admin/warehouse/issue.html",
        context,
    )

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        "warehouse",
        "product",
        "quantity",
        "updated_at",
    )

    list_filter = ("warehouse",)

    search_fields = (
        "product__title",
        "warehouse__title",
    )

    readonly_fields = (
        "warehouse",
        "product",
        "quantity",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
@admin.register(StockReceipt)
class StockReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "warehouse",
        "product",
        "quantity",
        "supplier",
        "received_at",
    )

    list_filter = (
        "warehouse",
        "received_at",
    )

    search_fields = (
        "product__title",
        "warehouse__title",
        "supplier",
    )

    readonly_fields = (
        "warehouse",
        "product",
        "quantity",
        "supplier",
        "comment",
        "received_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    


@admin.register(StockIssue)
class StockIssueAdmin(admin.ModelAdmin):
    list_display = (
        "warehouse",
        "product",
        "quantity",
        "reason",
        "created_at",
    )

    list_filter = (
        "warehouse",
        "reason",
    )

    search_fields = (
        "product__title",
        "warehouse__title",
    )

    readonly_fields = (
        "warehouse",
        "product",
        "quantity",
        "reason",
        "comment",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False