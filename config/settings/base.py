"""
Django settings for template project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""


import os

import environ


ROOT_DIR = environ.Path(__file__) - 3  # (template/config/settings/base.py - 3 = template/)
APPS_DIR = ROOT_DIR.path('life_insurance_bank')
LOCALE_PATHS = ['{}/{}'.format(ROOT_DIR, 'locale')]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')

API_DOCS_PATH = '/api-docs/'

# ------------------------------------------------------------------------------
# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles'
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
]

# Apps specific for this project go here.
LOCAL_APPS = [
    'life_insurance_bank',
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'utils.middlewares.LoggingMiddleware'
]

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', default=False)
LOG_LEVEL = 'DEBUG' if DEBUG else env.bool('DJANGO_LOG_LEVEL', default='INFO')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(message)s',
            'datefmt': '[%d/%b/%Y %H:%M:%S]'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'life_insurance_bank': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        }
    }
}

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])
# END SITE CONFIGURATION

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# Uses django-environ to accept uri format
# See: https://django-environ.readthedocs.io/en/latest/#supported-types

# database_url_default = 'sqlite:///{}'.format(str(ROOT_DIR.path('db.sqlite3')))

# DOCKER AND MIGRATION
# ------------------------------------------------------------------------------
# docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD='mysecret' -d postgres:10.6
#
# migrating the database to dev.

DATABASES = {'default': env.db_url('DATABASE_URL', default=f'sqlite:///{os.path.join(BASE_DIR, "db.sqlite3")}')}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'pt-br'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
        'user': '100000/day',
    },
    'EXCEPTION_HANDLER': 'utils.utils.custom_exception_handler'
}

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'


# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = env.bool('DJANGO_CORS_ORIGIN_ALLOW_ALL', default=True)


default_headers = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)


# Storage - S3
# ------------------------------------------------------------------------------
STORAGE_BUCKET_NAME = env.str('STORAGE_BUCKET_NAME', default='cadun-core-dev')
STORAGE_USERNAME = env.str('STORAGE_USERNAME', default='F3T98N2JHOJKZU64M6OE')
STORAGE_PASSWORD = env.str('STORAGE_PASSWORD', default='uuG1DfuU74P3fznHYCGDr3iGn2FeIGvhPLqhdJq2')
STORAGE_PREFIX_NAME = env.str('STORAGE_PREFIX_NAME', default='upload/')
STORAGE_URL = env.str('STORAGE_URL', default='https://ceph-int.nexxera.com')
