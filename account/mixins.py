from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


class PreventSingUpMixin(AccessMixin):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('store:home')
        return super().dispatch(request, *args, **kwargs)