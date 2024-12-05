"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.http import HttpResponseRedirect

from dotenv import load_dotenv
import os
from urllib.parse import urljoin

from app import settings

load_dotenv()


def external_redirect_view(request, path):
    target_site = os.getenv('MY_REDIRECT_URL')
    redirect_url = urljoin(target_site, path)
    return HttpResponseRedirect(redirect_url)


urlpatterns = [
    path('new-site/', include([
        path('admin/', admin.site.urls),
        path('', include('main.urls', namespace='main')),
        path('catalog/', include('goods.urls', namespace='goods')),
        path('cart/', include('carts.urls', namespace='cart')),
    ])),

    re_path(r'^(?P<path>.*)$', external_redirect_view),
]

handler404 = 'main.views.handle_page_not_found'

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
