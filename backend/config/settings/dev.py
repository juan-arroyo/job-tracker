from .base import *

# Debug mode enabled in development — shows detailed error pages
# with stack traces. NEVER set to True in production.
DEBUG = True

# In development, accept requests from localhost only.
# Django's dev server is not exposed to the internet.
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Local PostgreSQL running in the db container via docker-compose.
# Credentials match those defined in docker-compose.yml.
# In production these come from a Kubernetes Secret instead.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='jobtracker'),
        'USER': config('DB_USER', default='jobtracker'),
        'PASSWORD': config('DB_PASSWORD', default='jobtracker'),
        'HOST': config('DB_HOST', default='db'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# In development, emails are printed to the console instead of sent.
# Useful for testing registration flows without a real email server.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Tell Django to trust requests coming through Nginx proxy on localhost
# Without this, Django rejects POST requests (login, logout, forms) with 403 CSRF error
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']