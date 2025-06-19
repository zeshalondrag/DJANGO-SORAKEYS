from decimal import Decimal
from django.conf import settings
from digital_store.models import Product, ProductType

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        keys = self.cart.keys()
        product_ids = {int(key.split(':')[0]) for key in keys}
        product_type_ids = {int(key.split(':')[1]) for key in keys if ':' in key}

        products = Product.objects.filter(pk__in=product_ids).select_related('seller').prefetch_related('discount_set')
        product_types = ProductType.objects.filter(pk__in=product_type_ids)
        
        product_dict = {p.pk: p for p in products}
        product_type_dict = {pt.pk: pt for pt in product_types}

        for key, item in self.cart.items():
            product_id, product_type_id = map(int, key.split(':'))
            if product_id in product_dict and product_type_id in product_type_dict:
                item['product'] = product_dict[product_id]
                item['product_type'] = product_type_dict[product_type_id]
                item['original_price'] = Decimal(item['original_price'])
                item['discounted_price'] = Decimal(item['discounted_price'])
                item['total_original_price'] = item['original_price'] * item['count']
                item['total_discounted_price'] = item['discounted_price'] * item['count']
                yield item

    def __len__(self):
        return sum(item['count'] for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product, product_type, count=1, update_count=False):
        key = f"{product.id}:{product_type.id}"
        discounted_price = product.get_discounted_price()
        original_price = product.price
        if key not in self.cart:
            self.cart[key] = {
                'count': 0,
                'original_price': str(original_price),
                'discounted_price': str(discounted_price),
                'product_id': str(product.id),
                'product_type_id': str(product_type.id)
            }
        current_count = self.cart[key]['count']
        if update_count:
            self.cart[key]['count'] = count
        else:
            self.cart[key]['count'] = current_count + count
        if self.cart[key]['count'] > product.stock:
            self.cart[key]['count'] = product.stock
        if self.cart[key]['count'] <= 0:
            self.remove(product, product_type)
        else:
            self.save()

    def remove(self, product, product_type):
        key = f"{product.id}:{product_type.id}"
        if key in self.cart:
            del self.cart[key]
            self.save()

    def get_total_original_price(self):
        return sum(Decimal(item['original_price']) * item['count'] for item in self.cart.values())

    def get_total_discounted_price(self):
        return sum(Decimal(item['discounted_price']) * item['count'] for item in self.cart.values())

    def clear(self):
        self.session.pop(settings.CART_SESSION_ID, None)
        self.session.modified = True