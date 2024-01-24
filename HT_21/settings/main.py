from settings.base import *


CLIENT_DATA_KEY = 'session_key'
CLIENT_CART_KEY = 'cart_key'

INSTALLED_APPS += [
    'rest_framework',

    'apps.accounts.apps.AccountConfig',
    'apps.cart.apps.CartConfig',
    'apps.products.apps.ProductConfig',
    'apps.scraper',
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },

}

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'
LOGIN_URL = 'login'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

TEMPLATES[0]['DIRS'].append('templates')
