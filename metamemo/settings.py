"""
Django settings for metamemo project.

Generated by 'django-admin startproject' using Django 3.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from decouple import Csv, config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


# Application definition

INSTALLED_APPS = [
    "metamemoapp",
    "timeline",
    "import_export",
    "blog",
    "django_summernote",
    "django_celery_results",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
if DEBUG:
    position = INSTALLED_APPS.index("blog")
    INSTALLED_APPS.insert(position, "debug_toolbar")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "metamemo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates/"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "metamemo.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    # TODO: change to use dj_database_url
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASS"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

# DATABASES = {
#    'default': {
#       'ENGINE': 'djongo',
#       'NAME': 'metamemo',
#    }
# }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR) + "/static"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DJANGO STORAGES
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL", default="")
AWS_S3_ACCESS_KEY_ID = config("AWS_S3_ACCESS_KEY_ID", default="")
AWS_S3_SECRET_ACCESS_KEY = config("AWS_S3_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="")

# CELERY SETTINGS

CELERY_RESULT_BACKEND = "django-db"


# METAMEMO SETTINGS

METAMEMO_LANGUAGE = "pt-BR"
FACEBOOK_COOKIES = config("FACEBOOK_COOKIES", default="")
FACEBOOK_PAGES = config("FACEBOOK_PAGES", default=0, cast=int)
FACEBOOK_PPP = config("FACEBOOK_PPP", default=0, cast=int)


GOOGLE_APPLICATION_CREDENTIALS = config("GOOGLE_APPLICATION_CREDENTIALS", default="")
GOOGLE_BLOGGER_CREDENTIALS = config("GOOGLE_BLOGGER_CREDENTIALS", default="")
GOOGLE_YOUTUBE_CREDENTIALS = config("GOOGLE_YOUTUBE_CREDENTIALS", default="")

CROWDTANGLE_FACEBOOK_API_KEY = config("CROWDTANGLE_FACEBOOK_API_KEY", default="")
CROWDTANGLE_INSTAGRAM_API_KEY = config("CROWDTANGLE_INSTAGRAM_API_KEY", default="")
