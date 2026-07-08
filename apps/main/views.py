from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.core.paginator import Paginator
from apps.main.models import Category, Product


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, "main/product/detail.html", {'product':product})

def product_list(request, category_slug=None):
    page_number = request.GET.get("page", 1)
    category = None
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(available=True)
    popular_product = Product.objects.filter(is_popular=True).order_by("-sold_count")[:8]
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, 8)
    page_obj= paginator.get_page(page_number)
    
    context = {
        "category": category,
        "categories":categories,
        "popular_product": popular_product,
        "products":page_obj.object_list,
        "product_page": page_obj,
        "category_slug": category_slug
    }
    return render(request, "main/product/list.html", context)

def about(request):
    return render(request, "main/about.html")


def contacts(request):
    return render(request, "main/contacts.html")


def delivery(request):
    return render(request, "main/delivery.html")


def returns(request):
    return render(request, "main/returns.html")