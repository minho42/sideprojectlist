from .base import *

DEBUG = False

ALLOWED_HOSTS += ["https://sideprojectlist.herokuapp.com", "https://sideprojectlist.co"]

# Sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://7e1ad01b17c94331b449f6ac42e8b34d@o410328.ingest.sentry.io/5494610",
    integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()],
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)


# Security
X_FRAME_OPTIONS = "DENY"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_SECONDS = 3600
SECURE_REFERRER_POLICY = "same-origin"


REDIS_URL = env("REDIS_URL")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
