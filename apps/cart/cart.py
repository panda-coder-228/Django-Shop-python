from decimal import Decimal
from apps.main.models import Product
from django.conf import settings


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def add(self, product, quantity=1, override_quantity=False):
        try:
            product_id = str(product.id)
            if not product_id in self.cart:
                self.cart[product_id] = {'quantity':0, 'price':str(product.price), 'discount':str(product.discount,) if hasattr(product, 'discount') else '0'}
            if override_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            if product_id in self.cart and self.cart[product_id]['quantity'] <= 0:
                del self.cart[product_id]
            self.save()
        except Exception as e:
            raise ValueError(f"Ошибка добовления товара:{e}")
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        product_ids = list(self.cart.keys())
        products = {str(product.id):product for product in Product.objects.filter(id__in=product_ids)}
        changed = False
        to_remove = []

        for product_id in product_ids:
            if product_id in products:
                self.cart[product_id]['product'] = products[product_id]
            else:
                to_remove.append(product_id)
                changed = True
        
        for product_id in to_remove:
            del self.cart[product_id]
        
        if changed:
            self.save()
        
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['discount'] = Decimal(item.get('discount', 0))
            item['discount_price'] = item['price'] - (item['price'] * item.get('discount', 0)) / Decimal('100').quantize(Decimal("0.01"))
            item['total_price'] = item['discount_price'] * item['quantity']
            yield item
        
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        total = Decimal('0')

        for item in self.cart.values():
            price = Decimal(item['price'])
            discount = Decimal(item.get('discount'))
            quantity = item['quantity']
            
            final_price = price - (price * discount) / Decimal('100')

            total += final_price * quantity
        return total.quantize(Decimal("0.01"))
    
    def clear(self):
        self.session.pop(settings.CART_SESSION_ID, None)
        self.session.modified = True