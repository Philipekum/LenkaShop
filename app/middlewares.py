import os
from dotenv import load_dotenv
from django.shortcuts import redirect
from django.conf import settings


load_dotenv()


class TemporaryRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redirect_url = os.getenv('MY_REDIRECT_URL')
        return redirect(redirect_url)
    
    def __call__(self, request):
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)
        
        if request.path.startswith('/new-site/'):
            return self.get_response(request)

        return redirect(os.getenv('MY_REDIRECT_URL'))
