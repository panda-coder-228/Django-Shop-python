from django.contrib import admin
from .models import Category, Product, ProductImage
from django.utils.html import format_html
from django.db.models import Sum
from django.urls import reverse


admin.site.site_header = "Glyse django shop"
admin.site.site_title = "My shop"
admin.site.index_title = "Welcome to the administration"


@admin.action(description="Зробити товар доступним")
def make_available(modeladmin, request, queryset):
    queryset.update(available=True)


@admin.action(description="Зробити товар не доступним")
def make_anavailable(modeladmin, request, queryset):
    queryset.update(available=False)


@admin.action(description="Убрати скидку")
def reset_discount(modeladmin, request, queryset):
    queryset.update(discount=0)



class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    ordering = ('number_position',)

    fields = [
        'preview',
        'images',
        'number_position'
    ]

    readonly_fields = ['preview']

    def preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img class="inline-preview-img" src="{}" '
                'width="70" height="70" '
                'style="border-radius:6px; object-fit:cover;">',
                obj.image.url
            )

        return "Нет фото"

    preview.short_description = "Фото товара"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    class Media:
        js = ("admin/js/image_preview.js",)

    list_display = (
        'title',
        'image_preview_category',
        'slug',
        'is_active',
        'created_at',
    )

    search_fields = ('title',)
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_active',)

    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "title",
                    "slug",
                    "image_category",
                    "image_preview_category",
                    "is_active",
                )
            },
        ),
    )

    readonly_fields = ("image_preview_category",)

    def image_preview_category(self, obj):
        if obj and obj.image_category:
            return format_html(
                '<img class="main-image-category" '
                'src="{}" '
                'style="width:90px; height:90px; '
                'object-fit:cover; '
                'border-radius:6px;">',
                obj.image_category.url
            )

        return "Нет фото"

    image_preview_category.short_description = "Фото"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    class Media:
        js = ("js/image_preview.js",)

    list_display = ('image_tag', 'slug','sku', 'title', 'description', 'available', 'stock_quantity', 'price',
                    'discount', 'final_price', 'delete_link', 'created_at', 'updated_at', 'is_popular')
    list_editable = ('price', 'available', 'description', 'is_popular')
    search_fields = ('category__title', 'title', 'slug', 'created_at',)
    list_filter = ('created_at', 'updated_at',)
    list_per_page = 10
    inlines = [ProductImageInline]
    actions = [make_anavailable, make_available, reset_discount]
    fieldsets = [
        ("Основна", {'fields': ['image_tag', 'title',
         'slug', 'category', 'description', 'final_price']}),
        ("Зображення", {'fields': ['image', "main_image_preview"]}),
        ("Ціна", {'fields': ['price', 'discount']}),
        ("Статус", {'fields': ['available']}),
        ("Параметри системи", {'fields': [
            'created_at', 'updated_at'], 'classes': ('collapse', )})
    ]
    readonly_fields = [
        'main_image_preview',
        'image_tag',
        'final_price',
        'created_at',
        'updated_at',
    ]
    prepopulated_fields = {'slug': ('title',)}
    

    @admin.display(description="Кількість")
    def stock_quantity(self, obj):
        return obj.stocks.aggregate(total=Sum("quantity"))["total"] or 0


    def main_image_preview(self, obj):
        if obj and obj.image:
            return format_html(
            '<img id="main-image-preview" src="{}" '
            'style="width:120px; height:150px; '
            'object-fit:cover; '
            'border-radius:8px; '
            'box-shadow:0 4px 10px rgba(0,0,0,0.25);">',
            obj.image.url,
        )

        return "Нет фото"


    main_image_preview.short_description = "Головне фото"


    def image_tag(self, obj):
        if obj and obj.image:
            url = reverse(
            "admin:main_product_change",
            args=[obj.pk]
        )

            return format_html(
            '<a href="{}">'
            '<img src="{}" width="50" height="60" '
            'style="border-radius:6px; object-fit:cover;">'
            '</a>',
            url,
            obj.image.url
        )

        return "-"


    image_tag.short_description = "Фото"
    image_tag.admin_order_field = "image"


    def delete_link(self, obj):
        if obj and obj.pk:
            url = reverse(
                "admin:main_product_delete",
                args=[obj.pk]
        )

            return format_html(
            '<a href="{}">Видалити</a>',
            url)

        return "-"


    delete_link.short_description = "Видалити"


    def final_price(self, obj):
        if obj and obj.discount and obj.discount > 0:
            return format_html(
            '<span style="color:#d9534f; font-weight:600;">{} грн</span>',
            obj.sell_price
        )

        return format_html(
        '<span style="color:#5cb85c; font-weight:600;">{} грн</span>',
        obj.price
    )


    final_price.short_description = "Фінальна ціна"
    final_price.admin_order_field = "price"
