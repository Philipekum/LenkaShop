import os
from dotenv import load_dotenv
from django.shortcuts import redirect


load_dotenv(override=True)


class TemporaryRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.redirect_enabled = os.getenv('MY_REDIRECT', 'False').lower() == 'true'
        self.redirect_url = os.getenv('MY_REDIRECT_URL')

    def __call__(self, request):
        if not self.redirect_enabled:
            return self.get_response(request)

        if request.path.startswith(('/static/', '/media/', '/favicon.ico')):
            return self.get_response(request)

        if request.path.startswith('/new-site/'):
            return self.get_response(request)

        if not self.redirect_url:
            return self.get_response(request)

        return redirect(self.redirect_url, permanent=False)
