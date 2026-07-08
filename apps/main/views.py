from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.core.paginator import Paginator
from apps.main.models import Category, Product


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, "main/product/detail.html", {'product':product})

def product_list(request, category_slug=None):
    number_page = request.GET.get("page", 1)
    category = None
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(available=True)
    popular_product = Product.objects.filter(is_popular=True).order_by("-sold_count")[:8]
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, 10)
    obj_page = paginator.get_page(number_page)
    
    context = {
        "category": category,
        "categories":categories,
        "popular_product": popular_product,
        "products":obj_page.object_list,
        "obj_page": obj_page,
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