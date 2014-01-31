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
print " base dir: " + BASE_DIR


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u%q(yzd%4s(5qyjui08!&!6dbjphzia^3^-*95h+r=$jr5%j!1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'kraken.urls'

WSGI_APPLICATION = 'kraken.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'kraken/static'),
)


# Template dir
TEMPLATE_DIRS = (
  os.path.join(BASE_DIR, 'status/templates'),
)

# Ceph REST URLS
CEPH_BASE_URL = 'http://localhost:5000/api/v0.1/'

CEPH_URLS = {
  'fsid': CEPH_BASE_URL + 'fsid',
  'cluster_health': CEPH_BASE_URL + 'health',
  'monitor_status': CEPH_BASE_URL + 'mon_status',
  'osd_listids': CEPH_BASE_URL + 'osd/ls',
  'pools': CEPH_BASE_URL + 'osd/lspools',
  'pool_details': CEPH_BASE_URL + 'osd/pool/get?var=pg_num&pool=',
  'pool_details_dump': CEPH_BASE_URL + 'pg/dump_pools_json',
  'osd_tree': CEPH_BASE_URL + 'osd/tree',
  'pg_status': CEPH_BASE_URL + 'pg/stat',
  'pg_map': CEPH_BASE_URL + 'pg/map?pgid=',
  'disk_free': CEPH_BASE_URL + 'df',
  'osd_stat': CEPH_BASE_URL + 'osd/stat',
  'report': CEPH_BASE_URL + 'report',
  'osd_details': CEPH_BASE_URL + 'osd/dump',
  'osd_perf': CEPH_BASE_URL + 'osd/perf',
  'crush_rule_dump': CEPH_BASE_URL + 'osd/crush/rule/dump',
  'crushmap': CEPH_BASE_URL + 'osd/getcrushmap',
}
