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



# назва, ціна, ІД, короткий опис
# (якщо є), бренд, категорія, лінка на продукт

# class SearsItem:
#     brand_name: str
#     name: str
#     partNum: str
#     source: str
#
#     additional_attributes_dict: dict
#
#     swatchesInd: bool
#     offer_id: str
#     upc: str
#     value_consumer_rating: str
#     text_consumer_rating: str
#
#     lowest_price: float
#     lowest_price_2: float
#     final_price: float
#     regular_price: float
#     price_dict: dict
#
#     show_cashback_badge: bool
#     cashback_badge_category: str
#     category: str
