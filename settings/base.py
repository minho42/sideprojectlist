from pathlib import Path

import django_heroku
import environ

import cloudinary

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = env("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []
# # <-- added for bebug_toolbar to appear
INTERNAL_IPS = ["localhost", "127.0.0.1"]


INSTALLED_APPS = [
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Third party apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # ... include the providers you want to enable:
    # "allauth.socialaccount.providers.google",
    # "allauth.socialaccount.providers.twitter",
    # "allauth.socialaccount.providers.github",
    "cloudinary",
    "crispy_forms",
    "crispy_tailwind",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    # Local apps
    "profiles",
    "project",
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {"SCOPE": ["profile", "email"], "AUTH_PARAMS": {"access_type": "online"}}
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # The WhiteNoise middleware should be placed directly after the Django SecurityMiddleware and before all other middleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sideprojectlist.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # `allauth` needs this from django
                "django.template.context_processors.request",
                # this allows navbar.html to access {{ MEDIA_URL }}
                "django.template.context_processors.media",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    # TODO Set this property for production
    "http://localhost:3000",
    "https://127.0.0.1:8080",
    "https://127.0.0.1:8000",
)

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAdminUser"],
    # "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}


SITE_ID = 1

WSGI_APPLICATION = "sideprojectlist.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "sideprojectlist",
        "USER": "sideprojectlistuser",
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        # "OPTIONS": {
        #     "min_length": 9,
        # },
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = "Side Project List <sideprojectlist@gmail.com>"
# Sendgrid
# https://sendgrid.com/docs/for-developers/sending-email/django/
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = env("SENDGRID_API_KEY")
EMAIL_PORT = "587"
EMAIL_USE_TLS = True

# allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "none"  # "mandatory", "optional", "none"
ACCOUNT_AUTHENTICATION_METHOD = "email"
# Using custom forms may ignore other allauth options set here unless handled manually in the custom forms
ACCOUNT_FORMS = {
    "login": "profiles.forms.LoginForm",
    "reset_password": "profiles.forms.UserResetPasswordForm",
    "signup": "profiles.forms.UserCreationForm",
}
ACCOUNT_ADAPTER = "profiles.models.CustomAccountAdapter"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 60
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
# ACCOUNT_USERNAME_MAX_LENGTH = 30  # This is my own. Not part of allauth settings -> commented out as length is not check upon signup because username is removed from signup
ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_USERNAME_BLACKLIST = []
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
SOCIALACCOUNT_ADAPTER = "profiles.models.CustomSocialAccountAdapter"
SOCIALACCOUNT_AUTO_SIGNUP = True

# crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# logout without confirmation
# Should convert GET to POST
ACCOUNT_LOGOUT_ON_GET = True

# custom user model
AUTH_USER_MODEL = "profiles.User"


# CELERY STUFF
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
# CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "Australia/ACT"
CELERY_TASK_SOFT_TIME_LIMIT = 1800


# https://django-csp.readthedocs.io/en/latest/
# https: // github.com/mozilla/django-csp
# django-csp, Content-Security-Policy
CSP_DEFAULT_SRC = ("'none'",)
# CSP_STYLE_SRC = ("'self'", "https://use.fontawesome.com", "https://code.jquery.com",
#                  "https://cdnjs.cloudflare.com/ajax/", "https://stackpath.bootstrapcdn.com/bootstrap", "https://code.jquery.com", "https://cdn.jsdelivr.net/npm/vue@2.6.0")
# CSP_SCRIPT_SRC_ELEM = ("'self'", "https://code.jquery.com")
# CSP_SCRIPT_SRC = ("'self'", "https://cdnjs.cloudflare.com/ajax/", )
CSP_IMG_SRC = ("'self'",)
CSP_FONT_SRC = ("'self'",)


CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

django_heroku.settings(locals())

cloudinary.config(
    cloud_name=env("CLOUDINARY_CLOUD_NAME"),
    api_key=env("CLOUDINARY_API_KEY"),
    api_secret=env("CLOUDINARY_API_SECRET"),
)
