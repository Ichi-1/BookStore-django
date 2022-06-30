from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import (
    CreateView,ListView,
    UpdateView,TemplateView, RedirectView
)

from orders.models import Order
from account.models import CustomUser
from .forms import SignUpForm, UserAccountUpdateForm
from .mixins import PreventSingUpMixin
from .token import token_generator


class SignUpView(SuccessMessageMixin, PreventSingUpMixin, CreateView):
    template_name = 'account/registration/signup.html'
    form_class = SignUpForm
    success_message = 'Account was created. Check your email for activation link'

    def form_valid(self, form):
        user = form.save(commit=False)    
        user.email = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password'])
        user.is_active = False 
        user.save()
        form.send_activation_email(self.request, user)
        return super(SignUpView, self).form_valid(form)


    def get_success_url(self):
        return reverse('account:login')


class AccountActivateView(RedirectView):
    url = reverse_lazy('account:success')
    
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return super().get(request, uidb64, token)
        else:
            return render(request, 'account/registration/activation_invalid.html')


class SuccessView(TemplateView):
    template_name = 'account/registration/success.html'


class UserDashboardView(LoginRequiredMixin, ListView):
    """
    Provide List of user orders and option for manage them
    """

    template_name = 'account/dashboard/dashboard.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user_id = self.request.user.id
        orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
        return orders


class UserAccountUpdateView(
        LoginRequiredMixin, 
        SuccessMessageMixin, 
        UpdateView
    ):

    model = CustomUser
    form_class = UserAccountUpdateForm
    template_name = 'account/dashboard/update.html'
    success_message = 'Profile Data Successfuly Updated'
    
    def get_success_url(self):
        return reverse('account:dashboard')







@login_required
def account_deactivate(request):
    user = CustomUser.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    # messages.info(request, 'Account successfuly deactivated')
    return redirect('account:deactivate_confirm')

