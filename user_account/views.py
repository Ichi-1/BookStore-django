from email import message
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site

from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import (
    CreateView,
    DetailView, DeleteView, 
    UpdateView, 
) 

from user_account.models import CustomUser
from .forms import SignUpForm, UserAccountUpdateForm
from .mixins import PreventSingUpMixin
from .token import token_service


class SignUpView(PreventSingUpMixin, CreateView):
    template_name = 'user_account/registration/signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save(commit=False)
        
        user.is_active = False # ??? 
        user.email = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password'])
        user.save()

        # setup email
        current_site = get_current_site(self.request)
        subject = 'Activate your account'
        message = render_to_string(
            'user_account/account_activation_link.html',{
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_service.make_token(user),
        })
        user.mail_service(subject=subject, message=message)
        
        return super(SignUpView, self).form_valid(form)


    def get_success_url(self):
        return reverse('user_account:dashboard')


class UserDashboardView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user_account/dashboard/dashboard.html'
    context_object_name = 'user'


class UserAccountUpdateView(
        LoginRequiredMixin, 
        SuccessMessageMixin, 
        UpdateView
    ):

    model = CustomUser
    form_class = UserAccountUpdateForm
    template_name = 'user_account/dashboard/update.html'
    success_message = 'Profile Data Successfuly Updated'
    
    def get_success_url(self):
        return reverse('user_account:dashboard', kwargs={'pk': self.object.pk})


# class UserAccountDeactivateView(
#         LoginRequiredMixin, 
#         SuccessMessageMixin, 
#         DeleteView
#     ):

#     model = CustomUser
#     template_name = 'user_account/delete.html'
#     success_message = 'Profile Data Successfuly Deactivated'


#     def form_valid(self, form):
#         pass


@login_required
def account_deactivate(request):
    user = CustomUser.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    # messages.info(request, 'Account successfuly deactivated')
    return redirect('user_account:deactivate_confirm')


def account_activate(request, uidb64, token):
    
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = CustomUser.objects.get(pk=uid)
  
    if (user is not None) and token_service.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('user_account:dashboard')
    else:
        return render(request, 'user_account/activation_invalid.html')
