"""
Django settings for apirest project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l-&rv#hckq#5k$oj!!6mp20gayzi2or8^o#w4awa8)bw1)ko47'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['delivery.simplelectronica.com','192.168.42.208','localhost','0.0.0.0','192.168.42.206','192.168.43.158','127.0.0.1','192.168.0.13','192.168.43.193']

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'dynamic_rest.renderers.DynamicBrowsableAPIRenderer',


    ),
    'DATE_FORMAT': "%d-%m-%Y",
    'TIME_FORMAT':"%H:%M:%S",
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'dynamic_rest',
    'app.apps.AppConfig',
    'fcm_django',
    'sslserver',
    'dbbackup',
    'django_crontab',

]
CRONJOBS = [
    ('00 13 * * *', 'app.cron.my_scheduled_job')
]
DBBACKUP_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DBBACKUP_STORAGE_OPTIONS = {
'oauth2_access_token': 'qxDmkC2oQ0AAAAAAAAAACIpJXwDA4OVZ0ronEVggJ40gZzoqRE_UlszhjBpbBMa-'
}
FCM_DJANGO_SETTINGS = {
        "FCM_SERVER_KEY":"AAAAGlskkQs:APA91bEuEoopOgOrCicNNwh83_8m0UhDFmP7fxlf9xtle8jyzLR8_3N4-XPVOdfSPwbUsjEIT4IkL-v8fVSVfRqAyzEMlAsAj1yJ9-Yh_ezyh8oQqMPUrpwbsz6SSDWJ0GMOmt0fzLvS",
         # true if you want to have only one active device per registered user at a time
         # default: False
        "ONE_DEVICE_PER_USER": False,
         # devices to which notifications cannot be sent,
         # are deleted upon receiving error response from FCM
         # default: False
        "DELETE_INACTIVE_DEVICES": False,
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'apirest.urls'

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

WSGI_APPLICATION = 'apirest.wsgi.application'
SENDSMS_BACKEND = 'app.mysmsbackend.SmsBackend'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'apirest_db',
        'USER': 'root',
        'PASSWORD': '5112734',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_L10N = False

USE_TZ = True

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'deliveryonpy@gmail.com'
EMAIL_HOST_PASSWORD = 'nosemeocurrenada+'
EMAIL_PORT = 587


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
