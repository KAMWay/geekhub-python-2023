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
