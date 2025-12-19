from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-6*cj4p75v#azsc*+w+459s&5^x804!=+@@*qr%$who@7luq&ko'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # --- APPS OBRIGATÓRIOS DO ALLAUTH ---
    'django.contrib.sites', # Necessário para autenticação social
    
    # --- TERCEIROS ---
    'rest_framework',
    'rest_framework.authtoken', # Necessário para dj-rest-auth
    'corsheaders',
    'django_filters',
    
    # --- AUTH & SOCIAL ---
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', # Provider do Google

    # --- SEUS APPS ---
    'api',
]

# Configuração do ID do Site (Necessário para o allauth)
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middleware do allauth (Obrigatório nas versões recentes)
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'setup.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'pt-br' # Mudei para português
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True

# --- CONFIGURAÇÕES DO DRF E AUTH ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Adicione esta linha (e não esqueça a vírgula no final):
        'rest_framework.authentication.TokenAuthentication', 
        
        # Pode manter o JWT se quiser suporte híbrido
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Configurações do DJ-REST-AUTH
REST_USE_JWT = True
# JWT_AUTH_COOKIE = 'my-app-auth'
# JWT_AUTH_REFRESH_COOKIE = 'my-app-refresh-token'

# Configurações do SIMPLE JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# --- CONFIGURAÇÕES CRUCIAIS DO ALLAUTH ---
# Define que o usuário pode logar com email ou username
ACCOUNT_LOGIN_METHODS = {'email', 'username'}

# Define que o email é obrigatório no cadastro
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True

# Para desenvolvimento: Imprimir emails no console (terminal) ao invés de enviar de verdade
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
