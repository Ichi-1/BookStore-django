from .basket import Basket
from apps.checkout.models import DeliveryOptions

def basket(request):
    return {
        'basket': Basket(request)
    }

def delivery_options(request):
    return {
        'delivery_options': DeliveryOptions.objects.filter(is_active=True)
    }