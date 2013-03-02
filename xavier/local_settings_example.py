import os
from settings import *

PROJECT_DIR = os.path.dirname(__file__)
TEST_PEP8_DIRS = [os.path.dirname(PROJECT_DIR), ]
TEST_PEP8_EXCLUDE = ['migrations', 'urls.py']

INSTALLED_APPS += ('test_pep8', )

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = '123'
