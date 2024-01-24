from django.db import models
from django.utils.translation import gettext_lazy as _


class ScrapyTask(models.Model):
    ids_str = models.TextField(_('IDS'))
