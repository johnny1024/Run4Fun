from .settings import *

SOUTH_TESTS_MIGRATE = False
DATABASES['default'] = {
    'NAME': 'test_db',
    'ENGINE': 'django.db.backends.sqlite3'
}
