import os, sys
from dotenv import load_dotenv


load_dotenv()

sys.path.insert(0, os.getenv('PROJECT_PATH'))
sys.path.insert(1, os.getenv('VENV_PATH'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
