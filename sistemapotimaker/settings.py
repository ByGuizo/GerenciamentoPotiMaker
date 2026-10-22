import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.utils.csp import CSP

BASE_DIR = Path(__file__).resolve().parent.parent


def carregar_arquivo_env(caminho):
    if not caminho.exists():
        return
    for linha in caminho.read_text(encoding='utf-8').splitlines():
        if '=' in linha:
            nome, valor = linha.split('=', 1)
            os.environ.setdefault(nome.strip(), valor.strip())


carregar_arquivo_env(BASE_DIR / '.env')


def lista_do_ambiente(nome):
    texto = os.environ.get(nome, '')
    return [parte.strip() for parte in texto.split(',') if parte.strip()]


DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
if not SECRET_KEY:
    raise ImproperlyConfigured('Defina a variável DJANGO_SECRET_KEY no arquivo .env.')

ALLOWED_HOSTS = lista_do_ambiente('DJANGO_ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = lista_do_ambiente('DJANGO_CSRF_TRUSTED_ORIGINS')

CONFIAR_X_REAL_IP = os.environ.get('DJANGO_CONFIAR_X_REAL_IP', 'False') == 'True'

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_HSTS_SECONDS', '0'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contas',
    'inventario',
    'projetos',
    'escala',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csp.ContentSecurityPolicyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sistemapotimaker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sistemapotimaker.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'contas.Usuario'

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']

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

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'login'

SESSION_COOKIE_AGE = 60 * 60 * 12

SECURE_CSP = {
    'default-src': [CSP.SELF],
    'script-src': [CSP.SELF],
    'style-src': [CSP.SELF, CSP.UNSAFE_INLINE, 'https://fonts.googleapis.com', 'https://cdnjs.cloudflare.com'],
    'font-src': [CSP.SELF, 'https://fonts.gstatic.com', 'https://cdnjs.cloudflare.com'],
    'img-src': [CSP.SELF, 'data:'],
    'form-action': [CSP.SELF],
    'frame-ancestors': [CSP.NONE],
    'base-uri': [CSP.SELF],
    'object-src': [CSP.NONE],
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simples': {'format': '{asctime} {levelname} {message}', 'style': '{'},
    },
    'handlers': {
        'arquivo': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'seguranca.log',
            'formatter': 'simples',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'potimaker': {'handlers': ['arquivo'], 'level': 'INFO'},
    },
}

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Recife'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
