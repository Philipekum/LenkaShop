from typing import Callable
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from app.settings import MY_REDIRECT, MY_REDIRECT_URL


class TemporaryRedirectMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if not MY_REDIRECT:
            return self.get_response(request)

        if request.path.startswith(('/static/', '/media/', '/favicon.ico')):
            return self.get_response(request)

        if request.path.startswith('/new-site/'):
            return self.get_response(request)
        
        if not MY_REDIRECT_URL:
            return self.get_response(request)

        return redirect(MY_REDIRECT_URL, permanent=False)
