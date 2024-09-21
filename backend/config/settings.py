import os, environ
from django.utils.translation import gettext_lazy as _

BASE_DIR = environ.Path(__file__) - 2
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
CONFIG_ROOT = os.path.join(BASE_DIR, 'config')

# read secret .env variables
env_file = os.path.join(BASE_DIR, '.env')
if not os.path.isfile(env_file):
    raise FileNotFoundError('Configuration file .env does not exist!')
env = environ.Env()
env.read_env(env_file)

DATABASES = {
    'default': env.db('DATABASE_URL'),
}

DEBUG = True
SECRET_KEY = env.str('SECRET_KEY')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'music.otasovo.cz']
CSRF_TRUSTED_ORIGINS = ['music.otasovo.cz'],

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'otasmusic',
    'embed_video',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'config.wsgi.application'

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


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'cs'

LANGUAGES = [
    ('cs', _('Czech')),
    ('en', _('English'))
]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "otasmusic/static"),
    os.path.join(BASE_DIR, "otasmusic/static/layout/edgpress")
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# CACHE_PATH = os.path.join(ROOT_PATH, '../..', "otasmusic/cache")
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': CACHE_PATH
#     },
#     'view': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': os.path.join(CACHE_PATH, "view"),
#     }
# }

DATE_FORMAT = 'd.m.Y'
TIME_FORMAT = 'H:i'

REGISTRATION_OPEN = True
ACCOUNT_ACTIVATION_DAYS = 1
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'

GOOGLE_RECAPTCHA_SECRET_KEY = env.str('GOOGLE_RECAPTCHA_SECRET_KEY')
YOUTUBE_API_KEY = env.str('YOUTUBE_API_KEY')
