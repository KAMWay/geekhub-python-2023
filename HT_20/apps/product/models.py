from django.db import models


# Create your models here.
class Product(models.Model):
    id = models.CharField(max_length=12, primary_key=True)

    brand_name = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    main_image_url = models.CharField(max_length=255)
    description = models.TextField()
    url = models.CharField(max_length=255)

    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    default_seller_id = models.CharField(max_length=12)
    store_id = models.IntegerField()

    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='products',
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name
