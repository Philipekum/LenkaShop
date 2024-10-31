from django.urls import path
from django.views.generic import DetailView

from main.views import *
from .models import InfoPage


class InfoPageDetailView(DetailView):
    model = InfoPage
    template_name = 'main/info_base.html'
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title  
        return context

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('<slug:slug>/', InfoPageDetailView.as_view(), name='info_page'),
]
