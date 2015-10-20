"""
Django settings for krakendash project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qcv3468b6n53bv53u5cnyp389bcn398nv5[1p46789bvnc8p35oi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'mathfilters',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'kraken.urls'

WSGI_APPLICATION = 'kraken.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'users.db'),
    #}
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = ''
STATIC_URL = '/krakendash/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'kraken/static'),
)


# Template dir
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'status/templates'),
    os.path.join(BASE_DIR, 'ops/templates'),
)


# Ceph REST URLS
CEPH_BASE_URL = 'http://127.0.0.1:5000/api/v0.1/'

S3_SERVERS = [
    'ceph1',
    'ceph2',
    'ceph3',
]
S3_ACCESS = ""
S3_SECRET = ""

