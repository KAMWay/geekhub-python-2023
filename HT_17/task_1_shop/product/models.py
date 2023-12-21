from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def to_dict(self):
        return {
            'name': self.name,
            'price': f'{self.price}',
            'description': f'{self.description}',
            'category_id': f'{self.category.id}',
        }

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def to_dict(self):
        return {
            'name': self.name,
        }

    def __str__(self):
        return self.name
