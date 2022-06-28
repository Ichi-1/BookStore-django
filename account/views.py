from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import (
    CreateView,
    DetailView,  
    UpdateView, 
    TemplateView
) 

from account.models import CustomUser
from .forms import SignUpForm, UserAccountUpdateForm
from .mixins import PreventSingUpMixin
from .token import token_generator


class SignUpView(SuccessMessageMixin, PreventSingUpMixin, CreateView):
    template_name = 'account/registration/signup.html'
    form_class = SignUpForm
    success_message = 'Your account was created successfully. Activation link sended'

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


class SuccessView(TemplateView):
    template_name = 'account/registration/success.html'


class UserDashboardView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'account/dashboard/dashboard.html'
    context_object_name = 'user'


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
        return reverse('account:dashboard', kwargs={'pk': self.object.pk})




@login_required
def account_deactivate(request):
    user = CustomUser.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    # messages.info(request, 'Account successfuly deactivated')
    return redirect('user_account:deactivate_confirm')


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:success')
    else:
        return render(request, 'account/registration/activation_invalid.html')
