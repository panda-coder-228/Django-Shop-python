from django.shortcuts import render, get_object_or_404, redirect
from apps.main.models import Product
from .forms import CartAddProductForm
from .cart import Cart
from .services import handle_cart_modification


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # Кнопки + и -
    if "quantity" in request.POST:
        quantity = int(request.POST.get("quantity", 0))
        override = request.POST.get("override", "False") == "True"

        handle_cart_modification(cart, product, quantity, override)
        return redirect("cart:cart_detail")

    # Добавление товара с карточки
    form = CartAddProductForm(request.POST)
    print(form.is_valid())
    print(form.errors)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd["quantity"],
            override_quantity=cd["override"],
        )

    return redirect("cart:cart_detail")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})