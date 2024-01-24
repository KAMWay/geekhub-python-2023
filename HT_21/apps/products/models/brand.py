from django.db import models
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)

    def __str__(self):
        return self.name
