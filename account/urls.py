from django.urls import path
from django.views.generic import TemplateView

from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .forms import (
    UserLoginForm, 
    PwdResetForm, PwdResetConfirmForm
)
from .views import (
    SuccessView,
    account_activate, 
    account_deactivate,
    SignUpView, UserAccountUpdateView,
    UserDashboardView, 
)


app_name = 'account'

urlpatterns = [
    # registration and login/logour resoureces
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', account_activate, name='activate'),
    path('success', SuccessView.as_view(), name='success'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(
        template_name='account/registration/login.html', 
        form_class=UserLoginForm), 
        name='login',
        
    ),
    
    # dashboard resources
    path('dashboard/<int:pk>', UserDashboardView.as_view(), name='dashboard'),
    path('update/<int:pk>', UserAccountUpdateView.as_view(), name='update'),
    path('deactivate/', account_deactivate, name='deactivate'),
    path('deactivate_confirm/', TemplateView.as_view(
            template_name='account/deactivate_confirm.html'
        ), 
        name='deactivate_confirm'
    ),

    # reset 
    path('reset-password/', 
        PasswordResetView.as_view(
            template_name='account/reset_password/reset_form.html',
            success_url='reset_confirm',
            email_template_name='account/reset_password/sent_email.html',
            form_class=PwdResetForm 
        ), 
        name='reset_password'
    ),

    path('reset_comfirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
            template_name='account/reset_password/confirm_form.html',
            success_url='password_reset_complete',
            form_class=PwdResetConfirmForm,
        ), 
        name='password_reset_confirm'
    ),



    path('reset-password/reset_confirm', 
        PasswordResetDoneView.as_view(
            template_name='account/reset_password/reset_status.html'
        ), 
        name='password_reset_done'
    ),
    
    path('password-reset-complete/', 
        PasswordResetCompleteView.as_view(
            template_name='account/reset_password/reset_status.html'
        ),
        name='password_reset_complete'
    )

]