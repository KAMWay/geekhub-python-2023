from settings.base import *

INSTALLED_APPS += [
    'apps.product.apps.ProductConfig'
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
