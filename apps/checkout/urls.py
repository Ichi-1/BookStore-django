from django.urls import path
from .views import (
    DeliveryOptionsList,
    basket_update_delivery,
    delivery_address,
    payment_selection,
    payment_complete,
    payment_successful,
)


app_name = 'checkout'


urlpatterns = [
    path('delivery_options/', DeliveryOptionsList.as_view(), name='delivery_options'),
    path('delivery_address/', delivery_address, name='delivery_address'),
    path('payment_selection/', payment_selection, name='payment_selection'),
    path('payment_complete/', payment_complete, name='payment_complete'),
    path('payment_successful/', payment_successful, name='payment_successful'),
    path('basket_update_delivery', basket_update_delivery, name='basket_update_delivery'),
]
