"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import os.path
import environs
from pathlib import Path
import logging

env = environs.Env()

env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.


BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('NEWSPAPER_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = ['.herokuapp.com', '127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'crispy_forms',
    'crispy_bootstrap5',
    'celery',
    'redis',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_filters',
    'debug_toolbar',
    'news_project.apps.NewsConfig',
    'sign.apps.SignConfig',
    'protect.apps.ProtectConfig',
    'django_apscheduler.apps.DjangoApschedulerConfig',
    'rest_framework',
    'drf_spectacular',
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'NewsPaper Project',
    'DESCRIPTION': 'A simple news and articles project',
    'VERSION': '1.0.0',
}

APSCHEDULER_DATETIME_FORMAT = 'N j, Y, f:s a'

APSCHEDULER_RUN_NOW_TIMEOUT = 25

SITE_ID = 1

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'news_project.middlewares.TimezoneMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'news_project.context_processors.navigate_context',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {'signup': 'sign.forms.CommonSignupForm'}
SOCIALACCOUNT_FORMS = {'signup': 'sign.socialforms.MyCustomSocialSignupForm'}
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_LOGIN_ON_GET = True

ACCOUNT_EMAIL_SUBJECT_PREFIX = '[NewsPaper]'

WSGI_APPLICATION = 'NewsPaper.wsgi.application'
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {

    "default": env.dj_db_url("DATABASE_URL")
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        'TIMEOUT': 30,
    }
}


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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # INFO format
        'i_format': {
            'style': '{',
            'format': '{asctime} | {levelname} | {module} | {message}',
        },
        # debug format
        'd_format': {
            'style': '{',
            'datetime': '%Y.%m.%d %H:%M:%S',
            'format': '{asctime} | {levelname} | {message}',
        },
        # warning format
        'w_format': {
            'style': '{',
            'datetime': '%Y.%m.%d %H:%M:%S',
            'format': '{asctime} | {levelname} | {pathname} | {message}',
        },
        # error and critical format
        'e_c_format': {
            'style': '{',
            'datetime': '%Y.%m.%d %H:%M:%S',
            'format': '{asctime} | {levelname} | {pathname} | {exc_info} |{message}',
        },
        'mail_format': {
            'style': '{',
            'datetime': '%Y.%m.%d %H:%M:%S',
            'format': '{asctime} | {levelname} | {pathname} | {message}',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'  # обрабатываем только когда параметр DEBUG = False в settings.py
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'  # обрабатываем только когда параметр DEBUG = True
        },
    },
    'handlers': {
        'console_i': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'i_format',
        },
        'console_d': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'd_format',
        },
        'console_w': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'w_format',
        },
        'console_e_c': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'e_c_format',
        },
        'general_log': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': 'logs/general.log',
            'formatter': 'i_format',
        },
        'error_log': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
            'formatter': 'e_c_format',
        },
        'security_log': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'i_format',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_true'],
            'formatter': 'mail_format',
        },
    },
    'loggers':{
        'django': {
            'handlers': ['console_i', 'general_log'],
            'level': 'DEBUG',
        },
        'console_debug': {
            'handlers': ['console_d'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'console_warning': {
            'handlers': ['console_w'],
            'level': 'WARNING',
            'propagate': False,
        },
        'console_e_c': {
            'handlers': ['console_e_c'],
            'level': 'ERROR',
            'propagate': False,
        },
        'file_general': {
            'handlers': ['general_log'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['error_log', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['error_log', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['error_log'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db_backends': {
            'handlers': ['error_log'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_log'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Русский'),
    ('fr', 'Français'),
]

TIME_ZONE = 'Europe/Moscow'

CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = TIME_ZONE

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [str(BASE_DIR.joinpath("static"))]

STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = 465
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True

ADMINS = [
    (env.str('ADMIN_NICKNAME'), env.str('ADMIN_EMAIL')),
]

SERVER_EMAIL = env.str('SERVER_EMAIL')

DEFAULT_FROM_EMAIL = env.str('SERVER_EMAIL')

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

CRISPY_TEMPLATE_PACK = 'bootstrap5'

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

INTERNAL_IPS = '127.0.0.1'

CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)

SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)

SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=2592000)

SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)

SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=True)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
