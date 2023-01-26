from . import *

DEBUG = False
ALLOWED_HOSTS = ['192.168.10.250', 'solistool.fr']
STATIC_ROOT = '/home/SolisArt_SAV/static/'
MEDIA_ROOT = '/home/SolisArt_SAV/media/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'SAV',
         'USER': 'postgres',
          'PASSWORD': 'SolisArt',
          'HOST': '192.168.10.250',
         'PORT': '5432',
    }
}