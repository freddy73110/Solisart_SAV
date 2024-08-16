from . import *

DEBUG = False
ALLOWED_HOSTS = ['192.168.10.250', 'solistool.fr']
STATIC_ROOT = '/home/SolisArt_SAV/static/'
MEDIA_ROOT = '/home/SolisArt_SAV/'
#nginx sites-available => gèrer le répertoire media au 03/03 cd /home/media
#pas sûr que MEDIA_ROOT serve

#En prod, redis est sur la même machine
broker_url = 'redis://localhost:6379'
result_backend = 'redis://localhost:6379'


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'SAV',
         'USER': 'postgres',
          'PASSWORD': 'SolisArt',
          'HOST': '192.168.10.250',
         'PORT': '5432',
    },
    'herakles':{
        'ENGINE': 'mssql',
         'NAME': 'DQE',
         'USER': 'sa',
          'PASSWORD': 'Her@kles',
          'HOST': '192.168.10.253\HERAKLES',
         'PORT': '',
        "OPTIONS": {
            "driver": "ODBC Driver 17 for SQL Server",
            'unicode_results': True
        },
    }
}