from apps.products.models import Product
from settings.main import CLIENT_DATA_KEY, CLIENT_CART_KEY


# Create your models here.

class Cart:
    def __init__(self, request):
        # self.session = request.session
        client_data = request.session.get(CLIENT_DATA_KEY)
        if not client_data:
            self.session[CLIENT_DATA_KEY] = client_data = {}

        cart = client_data.get(CLIENT_CART_KEY)
        if not cart:
            client_data[CLIENT_CART_KEY] = cart = []

        self.cart = cart

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart)

    def __iter__(self):
        all_product_ids = [item['product_id'] for item in self.cart]
        print(all_product_ids)
        products = Product.objects.filter(id__in=all_product_ids)

        cart = []
        for product in products:
            item = {
                'product': product,
                'quantity': self.__select_product(product.id)['quantity']
            }
            cart.append(item)

        total = 0
        for item in cart:
            item['total'] = item['product'].sale_price * int(item['quantity'])
            total += item['total']
            yield item

        self.total = total

    def update(self, product_id, product_quantity: int):
        for item in self.cart:
            print()

        item = self.__select_product(product_id)
        if item:
            item['quantity'] = product_quantity
        else:
            item = {
                'product_id': product_id,
                'quantity': product_quantity
            }
            self.cart.append(item)

        self.session.modified = True

    def __select_product(self, product_id: str) -> dict:
        for items in self.cart:
            if items['product_id'] == product_id:
                return items

    def delete(self, product_id):
        for i in range(len(self.cart)):
            if self.cart[i]['product_id'] == product_id:
                del self.cart[i]
                break

        self.session.modified = True

    def clear(self):
        del self.session[CLIENT_DATA_KEY][CLIENT_CART_KEY]
        self.session.modified = True

    def is_exist(self, product_id: str) -> bool:
        return True if self.__select_product(product_id) else False

    def product_quantity(self, product_id) -> int:
        return self.__select_product(product_id)['quantity']
