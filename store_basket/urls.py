from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('summary/', views.basket_summary, name='basket-summary'),
    path('add/', views.basket_add, name='basket-add'),
    path('delete/', views.basket_delete, name='basket-delete'),
    path('update/', views.basket_update, name='basket-update'),
]