from django import forms

from main.models import Product
from .choices import Reason
from .models import Warehouse


class StockReceiptForm(forms.Form):
    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.filter(is_active=True),
        label="Склад",
    )

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Товар",
    )

    quantity = forms.IntegerField(
        min_value=1,
        label="Кількість",
    )

    supplier = forms.CharField(
        required=False,
        label="Постачальник",
    )

    comment = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Коментар",
    )


class StockIssueForm(forms.Form):
    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.filter(is_active=True),
        label="Склад",
    )

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Товар",
    )

    quantity = forms.IntegerField(
        min_value=1,
        label="Кількість",
    )

    reason = forms.ChoiceField(
        choices=Reason.choices,
        label="Причина",
    )

    comment = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label="Коментар",
    )