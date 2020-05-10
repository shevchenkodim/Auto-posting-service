import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'iv#eaoo%l@c+lj)%xx+(2uenq=a!l8ex-(8q3mce0x%s&g$z9_'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'autoposting',
        'USER': 'djuser',
        'PASSWORD': 'djuser',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
