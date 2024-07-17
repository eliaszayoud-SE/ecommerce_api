from .common import *

DEBUG = True

SECRET_KEY = 'django-insecure-*6jc1nyf3_70^=*hf3itq4c6rrt^-2-m=vhz%z@60)gs^-(p(j'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}