import os, sys


sys.path.insert(0, '/var/www/u2775036/data/www/lnkstore.ru')
sys.path.insert(1, '/var/www/u2775036/data/venv3.9/lib/python3.9/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
