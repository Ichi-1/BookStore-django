from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import (
    CreateView,
    ListView,
    RedirectView,
    TemplateView,
    UpdateView,
)

from apps.account.models import Address, Customer
from apps.orders.models import Order
from apps.store.models import Product

from .forms import SignUpForm, UserAccountUpdateForm, UserAddressForm
from .mixins import PreventSingUpMixin
from .token import token_generator

# * Registration section


class SignUpView(PreventSingUpMixin, SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    template_name = 'account/registration/signup.html'
    success_message = (
        'Account was created. Check your email for activation link'
    )

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


class ActivateAccountView(RedirectView):
    url = reverse_lazy('account:success')

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Customer.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return super().get(request, uidb64, token)
        else:
            return render(
                request,
                'account/registration/activation_failed.html'
            )


class SuccessView(TemplateView):
    template_name = 'account/registration/activation_success.html'


@login_required
def deactivate_account(request):
    user = Customer.objects.get(name=request.user.name)
    user.is_active = False
    user.save()
    logout(request)
    messages.info(request, 'Account deactivated successfuly')
    return redirect('account:deactivate_confirm')


# * User Dashboard section

class UserDashboardView(LoginRequiredMixin, ListView):
    """
    Provide List of user orders and option for manage them
    """
    template_name = 'account/dashboard/dashboard.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user_id = self.request.user.id
        orders = Order.objects.filter(user_id=user_id, billing_status=True)
        return orders


class UserAccountUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = Customer
    form_class = UserAccountUpdateForm
    template_name = 'account/dashboard/update.html'
    success_message = 'Profile info was updated successfuly'

    def get_success_url(self):
        return reverse('account:update', kwargs={'pk': self.object.pk})


# * Addresses CRUD section

class AddressesListView(LoginRequiredMixin, ListView):
    template_name = 'account/dashboard/addresses.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        user = self.request.user
        addresses = Address.objects.filter(customer=user)
        return addresses


class AddressCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = UserAddressForm
    template_name = 'account/dashboard/address_update.html'
    success_message = 'Address was added succesfully'

    def form_valid(self, form):
        address_data = form.save(commit=False)
        address_data.customer = self.request.user
        address_data.save()
        return super(AddressCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('account:addresses')


class AddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = UserAddressForm
    template_name = 'account/dashboard/address_update.html'
    success_message = 'Address was updated successfuly'

    def get_object(self):
        customer = self.request.user
        return Address.objects.get(pk=self.kwargs.get('id'), customer=customer)

    def get_success_url(self):
        return reverse('account:addresses')


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user)
    address.delete()
    messages.warning(request, 'Address was deleted successfuly')
    return redirect("account:addresses")


@login_required
def set_default(request, id):

    Address.objects.filter(customer=request.user, default=True)\
        .update(default=False)

    Address.objects.filter(pk=id, customer=request.user)\
        .update(default=True)

    previous_url = request.META.get('HTTP_REFERER')
    if 'delivery_address' in previous_url:
        messages.info(request, 'Address was set as delivery address')
        return redirect('checkout:delivery_address')
    else:
        messages.info(request, 'Address was set as default')
        return redirect('account:addresses')


# * Wishlist section

class WishListView(LoginRequiredMixin, ListView):
    template_name = 'account/dashboard/wish_list.html'
    context_object_name = 'wishlist'

    def get_queryset(self):
        wishlist = Product.objects.filter(users_wishlist=self.request.user)
        return wishlist


# * this function can remove item from wishlist
@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    user_wishlist = product.users_wishlist.filter(id=request.user.id)

    if user_wishlist.exists():
        product.users_wishlist.remove(request.user)
        messages.warning(
            request,
            f'«{product.title}» has been removed from your Wish List'
        )
    else:
        product.users_wishlist.add(request.user)
        messages.success(
            request,
            f'«{product.title}» added to your Wish List'
        )

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class OrderListView(ListView):
    template_name = 'account/dashboard/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user_id = self.request.user.id
        orders = Order.objects.filter(user_id=user_id, billing_status=True)
        return orders
