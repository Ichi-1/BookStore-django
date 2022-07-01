import os
import json
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from store_basket.basket import Basket
from orders.views import payment_confirmation

@login_required
def BasketView(request):

    basket = Basket(request)
    # parse decimal
    total = int(str(basket.get_total_price()).replace('.', '')) 

    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='usd',
        metadata={'userid': request.user.id}
    )
    return render(request, 
        'payment/payment_form.html', {
            'client_secret': intent.client_secret, 
            'STRIPE_PUBLICK_KEY' : os.environ.get('STRIPE_PUBLICK_KEY'),
        }
    )


@csrf_exempt
def srtipe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), 
            stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Event handling
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)
    else:
        print(f'Unhandled event type {event.type}')
    
    return HttpResponse(status=200)


def order_placed(request):
    basket = Basket(request)
    basket.clear()

    return render(request, 'payment/orderplaced.html')


class ErrorView(TemplateView):
    template_name = 'payment/error.html'