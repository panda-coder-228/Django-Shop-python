def handle_cart_modification(cart, product, quantity, override):
    if quantity <= 0:
        cart.remove(product)
    else:
        cart.add(product=product, quantity=quantity, override_quantity=override)