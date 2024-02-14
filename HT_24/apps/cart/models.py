from apps.products.models import Product

# Create your models here.
CLIENT_DATA_KEY = 'session_key'
CLIENT_CART_KEY = 'cart_key'


class Cart:
    def __init__(self, request):
        self.session = request.session
        client_data = request.session.get(CLIENT_DATA_KEY)
        if not client_data:
            self.session[CLIENT_DATA_KEY] = client_data = {}

        items = client_data.get(CLIENT_CART_KEY)
        if not items or not self.__is_valid(items):
            client_data[CLIENT_CART_KEY] = items = []

        self.items = items

    def __len__(self):
        return sum(int(item['quantity']) for item in self.items)

    def __iter__(self):
        all_product_ids = [item['product_id'] for item in self.items]
        products = Product.objects.filter(id__in=all_product_ids)

        cart = []
        for product in products:
            item = {
                'product': product,
                'quantity': self.select_product(product.id)['quantity']
            }
            cart.append(item)

        total = 0
        for item in cart:
            item['total'] = item['product'].sale_price * int(item['quantity'])
            total += item['total']
            yield item

        self.total = total

    def __is_valid(self, cart):
        if cart is None:
            return False

        for item in cart:
            if not isinstance(item, dict):
                return False

            if not item.get('quantity', None) or not item.get('product_id', None):
                return False

        return True

    def update(self, product_id, product_quantity: int):
        item = self.select_product(product_id)
        if item:
            item['quantity'] = product_quantity
        else:
            item = {
                'product_id': product_id,
                'quantity': product_quantity
            }
            self.items.append(item)

        self.session.modified = True

    def select_product(self, product_id: str) -> dict:
        for items in self.items:
            if items['product_id'] == product_id:
                return items

    def delete(self, product_id):
        for i in range(len(self.items)):
            if self.items[i]['product_id'] == product_id:
                del self.items[i]
                break

        self.session.modified = True

    def clear(self):
        del self.session[CLIENT_DATA_KEY][CLIENT_CART_KEY]
        self.session.modified = True

    def is_exist(self, product_id: str) -> bool:
        return True if self.select_product(product_id) else False

    def product_quantity(self, product_id) -> int:
        return self.select_product(product_id)['quantity']
