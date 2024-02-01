from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(_('created date'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated date'), auto_now_add=True)

    class Meta:
        abstract = True
