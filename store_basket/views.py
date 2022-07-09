from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .basket import Basket
from store.models import Product


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/summary.html', {
        'basket': basket,
    })


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        # update basket
        basket.add(product=product, qty=product_qty)

        basket_qty = basket.__len__()

        response = JsonResponse({"qty": basket_qty,})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        basket.delete(product_id=product_id)

        basket_qty = basket.__len__()
        basket_subtotal = basket.get_total_price()

        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_subtotal})
        return response

        
    
def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        basket.update(product_id=product_id, qty=product_qty)


        basket_qty = basket.__len__()
        basket_subtotal = basket.get_total_price()

        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_subtotal})
        return response




        
# get_object_or_400 insead of :
        # try:
        #     product_id = Product.objects.get(id=product_id)
        # except:
        #     raise Http404()
