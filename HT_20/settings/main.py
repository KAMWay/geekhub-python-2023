from settings.base import *

INSTALLED_APPS += [
    'apps.account.apps.AccountConfig',
    'apps.cart.apps.CartConfig',
    'apps.product.apps.ProductConfig',
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

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

TEMPLATES[0]['DIRS'].append('templates')

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'
LOGIN_URL = 'login'

CLIENT_DATA_KEY = 'session_key'
CLIENT_CART_KEY = 'cart_key'
