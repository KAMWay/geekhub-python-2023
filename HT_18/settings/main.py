from settings.base import *

INSTALLED_APPS += [
    'apps.product.apps.ProductConfig'
]

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

TEMPLATES[0]['DIRS'].append('templates')
