#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

os.path.supports_unicode_filenames = True

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'ip2geo.context_processors.add_session',
)

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

ALLOWED_HOSTS = ['*']

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

# registration
ACCOUNT_ACTIVATION_DAYS = 2
AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = '****@gmail.com'
EMAIL_HOST_PASSWORD = '****'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = '****@gmail.com'
#------------------



MANAGERS = ADMINS


DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db',                # Or path to database file if using sqlite3.
        'USER': '****',                       # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }   
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru_RU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'media/'
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'
LOGIN_URL ='/accounts/login/'
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'media/'
DJANGO_WYSIWYG_FLAVOR = 'ckeditor'
DJANGO_WYSIWYG_MEDIA_URL = STATIC_URL + "ckeditor/"
CKEDITOR_UPLOAD_PATH = MEDIA_ROOT + u"/uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': 700,
    },
}


# Make this unique, and don't share it with anybody.
SECRET_KEY = '********'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'ip2geo.middleware.CityMiddleware',
    'django_geoip.middleware.LocationMiddleware',
)

ROOT_URLCONF = 'erp.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, "templates"),
)


# geo-location settings
# path to dat file
# Download this file in http://www.maxmind.com/app/geolitecity
GEOIP_DATA = os.path.join(PROJECT_PATH, "ip2geo/GeoLiteCity.dat")
# You can choose the following fields that will be stored in the session:
GEOIP_SESSION_FIELDS = ['country_name', 'country_code', 'country_code3', 'region_name', 'city', 'latitude', 'longitude', 'postal_code']
# You do not have to select all of them, for example:
GEOIP_SESSION_FIELDS = ['country_name', 'region_name', 'city',]

INSTALLED_APPS = (
    'erp.common',
    'bootstrap3',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'erp.user_management',
    'erp.employee_management',
    'erp.customer_management',
    'erp.news_management',
    'erp.photo_management',
    'django.contrib.admin',
    'erp.dashboard',
    'registration',
    'erp.avator_management',
    'captcha',
    'ckeditor',
    'erp.comment_management',
    'ip2geo',
    'django_geoip',
)

#set the default user profile
CUSTOM_USER_MODEL = 'user_management.UserProfile'

#add a trailing slash to each url
APPEND_SLASH = True
