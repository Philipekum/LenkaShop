from django.urls import path

from delivery.views import DeliveryDetails


app_name = 'delivery'


urlpatterns = [
    path("", DeliveryDetails.as_view(), name="delivery_details"),
]
