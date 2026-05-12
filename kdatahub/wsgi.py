"""
WSGI config for kdatahub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kdatahub.settings')

application = get_wsgi_application()
# Ensure WhiteNoise is aware of the static directory
static_dir = os.path.join(settings.BASE_DIR, 'static')
application = WhiteNoise(application, root=static_dir, autorefresh=True)
application.add_files(static_dir, prefix='static/')
