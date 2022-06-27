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
    SetNewPassWordForm,
    PasswordResetForm,
)
from .views import (
    account_activate, 
    account_deactivate,
    SignUpView, UserAccountUpdateView,
    UserDashboardView, 
)


app_name = 'user_account'

urlpatterns = [
    # registration and login/logour resoureces
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', account_activate, name='activate'),
    path('logout/', LogoutView.as_view(next_page='user_account:login'), name='logout'),
    path('login/', LoginView.as_view(
        template_name='user_account/registration/login.html', 
        form_class=UserLoginForm,
        redirect_authenticated_user=True), 
        name='login',
        
    ),
    
    # dashboard resources
    path('dashboard/<int:pk>', UserDashboardView.as_view(), name='dashboard'),
    path('update/<int:pk>', UserAccountUpdateView.as_view(), name='update'),
    path('deactivate/', account_deactivate, name='deactivate'),
    path('deactivate_confirm/', TemplateView.as_view(
        template_name='user_account/deactivate_confirm.html'), 
        name='deactivate_confirm'
    ),

    # password reset
    path('password_reset/', 
        PasswordResetView.as_view(
            form_class=PasswordResetForm,
            template_name='user_account/reset_password/password_reset_form.html',
            success_url='password_reset_email_confirm',
            email_template_name='user_account/reset_password/password_reset_email.html'), 
        name='pasword_reset'
    ),
    
    path('password_reset/password_reset_email_confirm/', 
        TemplateView.as_view(
            template_name='user_account/reset_password/reset_status.html'),
        name='password_reset_done',
    ),


    path('password_reset_confirm/<uidb64>/<token>', 
        PasswordResetConfirmView.as_view(
            template_name='user_account/reset_password/password_reset_confirm.html',
            success_url='/account/password_reset_complete/', 
            form_class=SetNewPassWordForm),
        name="password_reset_confirm"),
]