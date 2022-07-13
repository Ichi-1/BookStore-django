import os
from decouple import config
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ! SECURITY WARNING: keep the secret key used in production secret!
# ! SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps
    'apps.store',
    'apps.basket',
    'apps.account',
    'apps.orders',
    'apps.checkout',

    # 3rd party
    'crispy_forms',
    'mptt',
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

ROOT_URLCONF = 'ecommerce_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.store.context_processors.categories',
                'apps.basket.context_processors.basket',
                'apps.basket.context_processors.delivery_options'
            ],  
        },
    },
]

WSGI_APPLICATION = 'ecommerce_project.wsgi.application'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CRISPY_TEMPLATE_PACK = 'bootstrap4'


AUTH_USER_MODEL = 'account.Customer'
LOGIN_REDIRECT_URL = '/account/dashboard/'
LOGIN_URL = '/account/login/'
LOGOUT_REDIRECT_URL = LOGIN_URL


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# settings for stripe api
# stripe listen --forward-to 127.0.0.1:8000/payment/webhook/
# os.environ.setdefault('STRIPE_PUBLICK_KEY', STRIPE_PUBLICK_KEY)
STRIPE_ENDPOINT_SECRET = config('STRIPE_ENDPOINT_SECRET')
STRIPE_PUBLICK_KEY = config('STRIPE_PUBLICK_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')


# PayPal settings
PAYPAL_CLIENT_ID = config('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = config('PAYPAL_CLIENT_SECRET')

