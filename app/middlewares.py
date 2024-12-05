import os
from dotenv import load_dotenv
from django.shortcuts import redirect

load_dotenv()


class TemporaryRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redirect_url = os.getenv('MY_REDIRECT_URL')
        return redirect(redirect_url)
