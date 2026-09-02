from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%brl3m4-gz+$g_lv-oz0x9o+0%5%t0z7hxt)m*#7aq^9a%_mcr"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from .local import *
except ImportError:
    pass

LOGIN_URL = "/account/login/"
LOGIN_REDIRECT_URL = "/account/profile/"