from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.core.paginator import Paginator
from apps.main.models import Category, Product
from apps.cart.forms import CartAddProductForm


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart_add = CartAddProductForm()
    return render(request, "main/product/detail.html", {'product':product, "cart_add": cart_add})

def product_list(request, category_slug=None):
    page = request.GET.get("page", 1)
    category = None
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(available=True)
    popular_product = Product.objects.filter(is_popular=True).order_by("-sold_count")[:8]
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, 8)
    page_obj= paginator.get_page(page)
    
    cart_add = CartAddProductForm()

    context = {
        "category": category,
        "categories":categories,
        "popular_product": popular_product,
        "products":page_obj.object_list,
        "page_obj": page_obj,
        "category_slug": category_slug,
        "cart_add": cart_add,
    }
    return render(request, "main/product/list.html", context)

def about(request):
    return render(request, "main/pages/about.html")

def contacts(request):
    return render(request, "main/pages/contacts.html")


def delivery(request):
    return render(request, "main/pages/delivery.html")


def returns(request):
    return render(request, "main/pages/returns.html")