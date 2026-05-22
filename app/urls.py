from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from app import settings


URL_PREFIX = 'new-site'


urlpatterns = [
    path(f'{URL_PREFIX}/admin/', admin.site.urls),
    path(f'{URL_PREFIX}/', include('main.urls', namespace='main')),
    path(f'{URL_PREFIX}/catalog/', include('goods.urls', namespace='goods')),
    path(f'{URL_PREFIX}/cart/', include('carts.urls', namespace='cart')),
    path(f'{URL_PREFIX}/order/', include('orders.urls', namespace='orders')),
    path(f'{URL_PREFIX}/payments/',include('payments.urls', namespace='payments')),
]

handler404 = 'main.views.handle_page_not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT) # type: ignore[arg-type]
