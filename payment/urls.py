from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.BasketView, name='basket'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('webhook/', views.srtipe_webhook, name='webhook'),
    path('error/', views.ErrorView.as_view(), name='error'), 
]