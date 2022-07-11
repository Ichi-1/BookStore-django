import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView

from paypalcheckoutsdk.orders import OrdersGetRequest

from .paypal import PayPalClient
from .models import DeliveryOptions
from apps.orders.models import Order, OrderItem
from apps.basket.basket import Basket
from apps.account.models import Address

def p():
    pass


class DeliveryOptionsList(ListView):
    model = DeliveryOptions
    template_name = 'checkout/delivery_options.html'
    context_object_name = 'delivery_options'

    def get_qureyset(self):
        return DeliveryOptions.objects.filter(is_active=True)


@login_required
def basket_update_delivery(request):
    basket = Basket(request)

    if request.POST.get('action') == 'post':
        delivery_option = int(request.POST.get('delivery_option'))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)

        updated_total_price = basket.update_total_price(delivery_type.price)

        session = request.session
        if 'delivery' not in request.session:
            session['delivery'] = {'delivery_id': delivery_type.id}
        else:
            session['delivery']['delivery_id'] = delivery_type.id
            session.modified = True
        

        response = JsonResponse(
            {
                'total': updated_total_price,
                'delivery_price':delivery_type.price
            }
        )
        return response


@login_required
def delivery_address(request):
    session = request.session
    addresses = Address.objects.filter(customer=request.user).order_by('-default')

    if 'delivery' not in session:
        messages.warning(request, 'Please select delivery option')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    if 'address' not in session:
        session['address'] = {'address_id': str(addresses[0].id)}
    else:
        session['address']['address_id'] = str(addresses[0].id)
        session.modified = True

    return render(
        request, 
        'checkout/delivery_address.html', 
        {'addresses': addresses}
    )


@login_required
def payment_selection(request):
    delivery_address = Address.objects.filter(default=True).exists()

    if not delivery_address:
        messages.warning(request, 'Please select delivery address')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    return render(request, 'checkout/payment_selection.html', 
        {
            "PAYPAL_CLIENT_ID": settings.PAYPAL_CLIENT_ID,
        }
    )


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    print(body)

    data = body["orderID"]
    user_id = request.user.id

    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)

    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

    for item in basket:
        OrderItem.objects.create(
            order_id=order_id, 
            product=item["product"], 
            price=item["price"], 
            quantity=item["qty"]
        )

    return JsonResponse({'success': 'Return Something'})



@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()

    messages.success(request, 'Payment Successful!')
    return HttpResponseRedirect(reverse('account:order_list'))
