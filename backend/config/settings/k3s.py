from .base import *

# Debug must always be False in production —
# exposing stack traces to the public is a security risk
DEBUG = False

# Only accept requests coming through our domain.
# Requests to any other host will be rejected with 400 Bad Request.
# Domain for production traffic + worker IPs for direct debugging access
ALLOWED_HOSTS = ['demo.jmarroyo.es', '46.62.219.138', '77.42.124.22', '77.42.124.11']

CSRF_TRUSTED_ORIGINS = ['https://demo.jmarroyo.es']

# PostgreSQL credentials come from a Kubernetes Secret —
# never hardcoded here or in any file that goes to GitHub.
# The Secret injects them as environment variables into the Pod.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# In production, static files are served by Nginx directly —
# Django never handles static file requests in production.
# collectstatic copies all files to STATIC_ROOT for Nginx to serve.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# SSL redirect is handled by Traefik (Ingress Controller) —
# enabling it here would cause redirect loops
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True