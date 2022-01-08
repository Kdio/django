from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

"""
Django settings for asfetec project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

APP_NAME = 'ASFETEC'

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = 'app/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--(ag$4u+l$!%-aha_t11m3&kcq1tq)+%87ko5!em(+^%lan(^)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SESSION_COOKIE_AGE = 600 # one hour in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# Application definition

INSTALLED_APPS = [
    'app.apps.AppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'asfetec.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'asfetec.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASE_FILE = BASE_DIR / 'databases/asfetec.db'
DATABASE_FILE = BASE_DIR / 'databases/db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_FILE,
    }
}

MIGRATION_MODULES = {'app': 'databases.migrations'}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True
USE_L10N = False

USE_TZ = True

SHORT_DATE_FORMAT='d/m/Y'
DATE_FORMAT='d/m/Y'
DATE_INPUT_FORMATS=('%d/%m/%Y','%d-%m-%Y','%Y-%m-%d', '%m/%d/%Y')
DATETIME_FORMAT='d/m/Y H:M'
DATETIME_INPUT_FORMATS=('%d/%m/%Y %H:%M', '%Y-%m-%d %H:%M')
TIME_FORMAT='H:M'
TIME_INPUT_FORMATS=('%H:%M', '%H:%M:%S')
DECIMAL_SEPARATOR=','
THOUSAND_SEPARATOR='.'
USE_THOUSAND_SEPARATOR=True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# BOOTSTRAP5 Default settings
# BOOTSTRAP5 = {

#     # The complete URL to the Bootstrap CSS file
#     # Note that a URL can be either a string,
#     # e.g. "https://stackpath.bootstrapcdn.com/bootstrap/5.1.1/css/bootstrap.min.css",
#     # or a dict like the default value below.
#     # "css_url": {
#     #     "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css",
#     #     "integrity": "sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB",
#     #     "crossorigin": "anonymous",
#     # },

#     # The complete URL to the Bootstrap JavaScript file
#     # "javascript_url": {
#     #     "url": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js",
#     #     "integrity": "sha384-smHYKdLADwkXOn1EmN1qk/HfnUcbVRZyYmZ4qpPea6sjB/pTJ0euyQp0Mk8ck+5T",
#     #     "crossorigin": "anonymous",
#     # },

#     # The complete URL to the Bootstrap CSS file (None means no theme)
#     "theme_url": None,

#     # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap5.html)
#     'javascript_in_head': False,

#     # Label class to use in horizontal forms
#     'horizontal_label_class': 'col-md-3',

#     # Field class to use in horizontal forms
#     'horizontal_field_class': 'col-md-9',

#     # Set placeholder attributes to label if no placeholder is provided
#     'set_placeholder': True,

#     # Class to indicate required (better to set this in your Django form)
#     'required_css_class': '',

#     # Class to indicate error (better to set this in your Django form)
#     'error_css_class': 'is-invalid',

#     # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
#     'success_css_class': 'is-valid',

#     # Renderers (only set these if you have studied the source and understand the inner workings)
#     'formset_renderers':{
#         'default': 'bootstrap5.renderers.FormsetRenderer',
#     },
#     'form_renderers': {
#         'default': 'bootstrap5.renderers.FormRenderer',
#     },
#     'field_renderers': {
#         'default': 'bootstrap5.renderers.FieldRenderer',
#         'inline': 'bootstrap5.renderers.InlineFieldRenderer',
#     },
# }