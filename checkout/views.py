from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import DeliveryOptions
from store_basket.basket import Basket
from account.models import Address

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
    session = request.session

    if 'address' not in session:
        messages.warning(request, 'Please select delivery address')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    
    return render(request, 'checkout/payment_selection.html', {})