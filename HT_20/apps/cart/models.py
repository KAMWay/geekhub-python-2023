from apps.product.models import Product
from main import CLIENT_DATA_KEY, CLIENT_CART_KEY


# Create your models here.

class Cart:
    def __init__(self, request):
        self.session = request.session
        client_data = request.session.get(CLIENT_DATA_KEY)
        if not client_data:
            self.session[CLIENT_DATA_KEY] = client_data = {}

        cart = client_data.get(CLIENT_CART_KEY)
        if not cart:
            client_data[CLIENT_CART_KEY] = cart = {}

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

        total = 0
        for item in cart.values():
            item['total'] = item['product'].sale_price * int(item['quantity'])
            total += item['total']
            yield item

        self.total = total

    def update(self, product_id, product_quantity: int):
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = product_quantity
        else:
            self.cart[product_id] = {'quantity': product_quantity}

        self.session.modified = True

    def delete(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def clear(self):
        del self.session[CLIENT_DATA_KEY][CLIENT_CART_KEY]
        self.session.modified = True

    def is_exist(self, product_id) -> bool:
        return product_id in self.cart

    def product_quantity(self, product_id) -> int:
        return self.cart[product_id]['quantity']
