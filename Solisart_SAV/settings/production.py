from . import *

DEBUG = False
ALLOWED_HOSTS = ['192.168.10.250', 'solistool.fr']
STATIC_ROOT = '/home/SolisArt_SAV/static/'
MEDIA_ROOT = '/home/SolisArt_SAV/'
#nginx sites-available => gèrer le répertoire media au 03/03 cd /home/media
#pas sûr que MEDIA_ROOT serve
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
         'PORT': '1433',
        "OPTIONS": {
            "driver": "ODBC Driver 17 for SQL Server",
            'unicode_results': True,
            "setdecoding": [
                {"sqltype": pyodbc.SQL_CHAR, "encoding": 'latin-1'},
                {"sqltype": pyodbc.SQL_WCHAR, "encoding": 'latin-1'}],
            "setencoding": [
                {"encoding": "latin-1"}]
        },
    }
}