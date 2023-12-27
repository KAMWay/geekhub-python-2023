from settings.base import *

INSTALLED_APPS += [

]

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

TEMPLATES[0]['DIRS'].append('templates')
