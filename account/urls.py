from pipes import Template
from django.urls import path
from django.views.generic import TemplateView

from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView,
    PasswordResetConfirmView,
)
from .forms import (
    UserLoginForm, 
    PwdResetForm, PwdResetConfirmForm
)
from .views import (
    SuccessView,
    # account_activate, 
    account_deactivate,
    SignUpView, UserAccountUpdateView,
    UserDashboardView,
    AccountActivateView
)


app_name = 'account'

urlpatterns = [
    # registration and login/logour resoureces
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', AccountActivateView.as_view(), name='activate'),
    path('success', SuccessView.as_view(), name='success'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(
            template_name='account/registration/login.html', 
            form_class=UserLoginForm
        ),  name='login',
    ),
    
    # dashboard resources
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('update/<int:pk>', UserAccountUpdateView.as_view(), name='update'),
    path('deactivate/', account_deactivate, name='deactivate'),
    path('deactivate_confirm/', TemplateView.as_view(
            template_name='account/dashboard/deactivate_confirm.html'
        ),  name='deactivate_confirm'
    ),




    # reset process
    path('password_reset/', PasswordResetView.as_view(
            template_name='account/reset_password/reset_request_form.html',
            success_url='password_reset_email_confirm',
            email_template_name='account/reset_password/sent_email.html',
            form_class=PwdResetForm 
        ),  name='password_reset'
    ),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
            template_name='account/reset_password/confirm_form.html',
            success_url='complete',
            form_class=PwdResetConfirmForm,
        ),  name='password_reset_confirm'
    ),
    path('password_reset/password_reset_email_confirm/', TemplateView.as_view(
            template_name='account/reset_password/reset_status.html',
        ),  name='password_reset_done'
    ),
    path('password_reset_confirm/<uidb64>/set-password/complete', TemplateView.as_view(
            template_name='account/reset_password/reset_status.html',
        ),  name='password_reset_complete'
    )

]