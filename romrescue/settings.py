"""Django settings for romrescue project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""


# Standard Library
import os

# Django
from django.core.exceptions import FieldDoesNotExist
from django.db import models

# Third Party
import dj_database_url
import rollbar
from easy_thumbnails.conf import Settings as thumbnail_settings

models.FieldDoesNotExist = FieldDoesNotExist

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_ROOT = os.path.dirname(__file__)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")
STATIC_URL = "/static/"

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static"),)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "%^lk@u&&mb-89_t6_*&z08dif8m-tf15cphny1gy2&dvnf)#5_"

# SECURITY WARNING: don't run with debug turned on in production!

TESTING = os.environ.get("CI") == "true"
DEBUG = os.environ.get("ENV") != "production" or TESTING

ALLOWED_HOSTS = ["*"]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, "uploads")
CKEDITOR_URL = MEDIA_URL
CKEDITOR_JQUERY_URL = "//ajax.googleapis.com/" "ajax/libs/jquery/2.1.1/jquery.min.js"

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_HOST_USER = "apikey"
    EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_API_KEY")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.redirects",
    "django.contrib.sitemaps",
    "storages",
    "django_extensions",
    "debug_toolbar",
    "easy_thumbnails",
    "image_cropping",
    "crispy_forms",
    "crispy_bootstrap5",
    "polymorphic_tree",
    "polymorphic",
    "mptt",
    "ckeditor",
    "ckeditor_uploader",
    "adminsortable2",
    "sorl.thumbnail",
    "solo",
    "websettings",
    "modulestatus",
    "pages",
    "dogs",
    "team",
    "testimonials",
    "donate",
]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
]

ROOT_URLCONF = "romrescue.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [f"{BASE_DIR}/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "pages.context_processors.nav_items",
                "django.template.context_processors.request",
            ],
        },
    }
]


WSGI_APPLICATION = "romrescue.wsgi.application"

STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
THUMBNAIL_DEFAULT_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
THUMBNAIL_DEFAULT_STORAGE_ALIAS = "default"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "romrescue"
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = (
    "django.core.files.storage.FileSystemStorage" if DEBUG else "storages.backends.s3boto3.S3Boto3Storage"
)

NOSE_ARGS = [
    "--with-coverage",
    "--cover-package=romrescue,pages,dogs,team",
]

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DB_USER = os.environ.get("SNAP_DB_PG_USER") or "romrescue"
DB_PASS = os.environ.get("SNAP_DB_PG_PASSWORD") or "romrescue"
DB_HOST = os.environ.get("SNAP_DB_PG_HOST") or "127.0.0.1"
DB_NAME = "romrescue"

if "CIRCLECI" in os.environ:
    DB_NAME = "circle_test"
    DB_USER = "circleci"
    DB_PASS = ""
    DB_HOST = "127.0.0.1"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASS,
        "HOST": DB_HOST,
    }
}

if os.environ.get("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config(conn_max_age=600)

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": ("django.contrib.auth.password_validation." "UserAttributeSimilarityValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation." "NumericPasswordValidator"),
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True


USE_TZ = True

THUMBNAIL_PROCESSORS = ("image_cropping.thumbnail_processors.crop_corners",) + thumbnail_settings.THUMBNAIL_PROCESSORS

SITE_ID = 2

CRISPY_TEMPLATE_PACK = "bootstrap5"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


ROLLBAR = {
    "access_token": os.environ.get("ROLLBAR_ACCESS_TOKEN"),
    "environment": "development" if DEBUG else "production",
    "root": BASE_DIR,
}
if not DEBUG:
    rollbar.init(**ROLLBAR)


DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CSRF_TRUSTED_ORIGINS = [
    "https://www.romrescue.org/",
    "http://www.romrescue.org/",
    "http://*.romrescue.org",
    "https://*.romrescue.org",
]
