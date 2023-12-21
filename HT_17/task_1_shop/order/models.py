from django.db import models

from product.models import Product


# Create your models here.

class Order(models.Model):
    order_date = models.DateTimeField("date published")
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def info(self):
        return f'Order {self.id}'

    def __str__(self):
        return f'Order {self.id}'


class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'Order {self.order.id}: {self.product_quantity} x {self.product.name}'
