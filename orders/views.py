from urllib import response
from django.shortcuts import render
from django.http.response import JsonResponse

from store_basket.basket import Basket
from .models import Order, OrderItem


def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        user_id = request.user.id
        order_key = request.POST.get('order_key')
        basket_total = basket.get_total_price()

        # check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id, 
                full_name='name',
                address1='address1',
                address2='address2',
                total_paid=basket_total,
                order_key=order_key
            )
            order_id = order.pk
            # loop through session data, 
            # collecting each item the user has inside of their session
            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['qty']
                )
            
            response = JsonResponse({'success': 'Return Something'})
            return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)

