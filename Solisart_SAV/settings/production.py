from . import *

DEBUG = False
ALLOWED_HOSTS = ['192.168.10.250']
STATIC_ROOT = '/home/Solisart_SAV/static/'
MEDIA_ROOT = '/home/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'SAV',
         'USER': 'postgres',
         # 'PASSWORD': 'G2poilOQ!',
         # 'HOST': '127.0.0.1',
          'PASSWORD': 'SolisArt',
          'HOST': '192.168.10.250',
         'PORT': '5432',
    }
}