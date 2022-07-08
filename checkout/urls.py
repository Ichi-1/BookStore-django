from django.urls import path
from .views import (
    p, 
    DeliveryOptionsList,
    basket_update_delivery,
    delivery_address,
    payment_selection,
)


app_name = 'checkout'


urlpatterns = [
    path('delivery_options/', DeliveryOptionsList.as_view(), name='delivery_options'),
    path('delivery_address/', delivery_address, name='delivery_address'),
    path('payment_selection/', payment_selection, name='payment_selection'),
    # path('payment_complete/', p, name='payment_complete'),
    # path('payment_successful/', p, name='payment_successful'),
    path('basket_update_delivery', basket_update_delivery, name='basket_update_delivery'),
]