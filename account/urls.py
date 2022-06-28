from django.urls import path
from django.views.generic import TemplateView

from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
)
from .forms import (
    UserLoginForm, 
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
        template_name='account/deactivate_confirm.html'), 
        name='deactivate_confirm'
    ),

]