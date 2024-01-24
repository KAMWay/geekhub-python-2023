from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    id = models.CharField(_('id'), max_length=12, primary_key=True)

    name = models.CharField(_('name'), max_length=255)
    main_image_url = models.CharField(_('image url'), max_length=255)
    description = models.TextField(_('description'), )
    url = models.CharField(_('url'), max_length=255)

    regular_price = models.DecimalField(_('regular_price'), max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(_('sale_price'), max_digits=10, decimal_places=2)

    default_seller_id = models.CharField(_('default seller id'), max_length=12)
    store_id = models.IntegerField(_('store id'), )

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

    brand = models.ForeignKey(
        'Brand',
        on_delete=models.PROTECT,
        blank=True,
        related_name='products'
    )

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
        # if not self.slug:
        #     self.slug = slugify(str(f''))
        # super().save(*args, **kwargs)
