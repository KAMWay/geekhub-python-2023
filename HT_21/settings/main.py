from settings.base import *

CLIENT_DATA_KEY = 'session_key'
CLIENT_CART_KEY = 'cart_key'

INSTALLED_APPS += [
    # third part
    'django_extensions',
    'drf_spectacular',
    'rest_framework',

    # 'rest_framework.authtoken'

    # project
    'apps.accounts.apps.AccountConfig',
    'apps.cart.apps.CartConfig',
    'apps.products.apps.ProductConfig',
    'apps.scraper',

    # project tags
    'apps.cart.templatetags.inside',
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
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.authentication.TokenAuthentication',
    # ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated'
        'rest_framework.permissions.AllowAny'
    ],

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'Project API',
    'DESCRIPTION': 'HT_21',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

TEMPLATES[0]['DIRS'].append('templates')
