from decimal import Decimal

from django.db import models


# Create your models here.
class Product(models.Model):
    id = models.CharField(max_length=10, primary_key=True)

    brand_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    main_image_url = models.CharField(max_length=150)
    description = models.TextField()
    url = models.CharField(max_length=100)

    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    default_seller_id = models.CharField(max_length=100)
    store_id = models.IntegerField()

    def __str__(self):
        return self.id


class Cart:
    CLIENT_DATA_KEY = 'session_key'
    CLIENT_CART_KEY = 'cart_key'

    def __init__(self, request):
        self.session = request.session
        client_data = request.session.get(self.CLIENT_DATA_KEY)
        if not client_data:
            self.session[self.CLIENT_DATA_KEY] = client_data = {}

        cart = client_data.get(self.CLIENT_CART_KEY)
        if not cart:
            client_data[self.CLIENT_CART_KEY] = cart = {}

        self.cart = cart

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def __iter__(self):
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)

        cart = {}
        for product in products:
            cart[str(product.id)] = {}
            cart[str(product.id)]['product'] = product
            cart[str(product.id)]['quantity'] = self.cart[product.id]['quantity']

        for item in cart.values():
            item['total'] = item['product'].sale_price * int(item['quantity'])
            yield item

    def update(self, product_id, product_quantity):
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = product_quantity
        else:
            self.cart[product_id] = {'quantity': product_quantity}

        self.session.modified = True

    def delete(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def is_exist(self, product_id) -> bool:
        return product_id in self.cart

    def size(self):
        return len(self.cart)
