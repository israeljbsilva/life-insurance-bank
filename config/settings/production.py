"""
Production Configurations
"""
from .base import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env('DJANGO_SECRET_KEY')

INSTALLED_APPS += ['gunicorn', ]


# Site's Security
# ------------------------------------------------------------------------------
# Clickjacking attacks use layered frames to mislead users into clicking on a different link from
# the one they think they are clicking on. Fortunately, newer browsers support an X-Frame-Options
# header that allows you to limit or prevent the display of your pages within a frame. Valid options
# are “DENY” or “SAMEORIGIN” - the former prevents all framing of your site, and the latter allows
# only sites within the same domain to frame.
# Unless you have a need for frames, your best bet is to set “X-Frame-Options: DENY” – and this is
# what SecurityMiddleware will do for all responses, if the SECURE_FRAME_DENY setting is True.
X_FRAME_OPTIONS = 'DENY'

# For sites that should only be accessed over HTTPS, you can instruct newer browsers to
# refuse to connect to your domain name via an insecure connection (for a given period of time)
# by setting the “Strict-Transport-Security” header. This reduces your exposure to some
# SSL-stripping man-in-the-middle (MITM) attacks.
# If set to a non-zero integer value, causes SecurityMiddleware to set the HTTP Strict
# Transport Security header on all responses that do not already have that header.
# https://docs.djangoproject.com/en/2.0/ref/middleware/#http-strict-transport-security
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_PRELOAD = True

# Additionally, if you set the SECURE_HSTS_INCLUDE_SUBDOMAINS setting to True, SecurityMiddleware
# will add the includeSubDomains tag to the Strict-Transport-Security header. This is recommended,
# otherwise your site may still be vulnerable via an insecure connection to a subdomain.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# To prevent the browser from guessing the content type, and force it to always use the type
# provided in the Content-Type header, you can pass the X-Content-Type-Options: nosniff header.
# SecurityMiddleware will do this for all responses if the SECURE_CONTENT_TYPE_NOSNIFF setting is True.
SECURE_CONTENT_TYPE_NOSNIFF = True

# To enable the XSS filter in the browser, and force it to always block suspected XSS attacks, you
# can pass the X-XSS-Protection: 1; mode=block header. SecurityMiddleware will do this for all
# responses if the SECURE_BROWSER_XSS_FILTER setting is True.
SECURE_BROWSER_XSS_FILTER = True

# If set to True, causes SecurityMiddleware to redirect all non-HTTPS requests to HTTPS (except
# for those URLs matching a regular expression listed in SECURE_REDIRECT_EXEMPT).
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)

# Using a secure-only session cookie makes it more difficult for network traffic sniffers to
# hijack user sessions
SESSION_COOKIE_SECURE = True

# Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal
# the CSRF token.
CSRF_COOKIE_SECURE = True


# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
