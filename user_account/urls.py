from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView
)

from .forms import UserLoginForm
from .views import (
    account_activate, 
    dashboard,
    SignUpView, UserUpdateView
)

app_name = 'user_account'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', account_activate, name='activate'),
    path('dashboard/', dashboard, name='dashboard'),
    path('update/', UserUpdateView.as_view(), name='update'),

    path('login/', 
            LoginView.as_view(
                template_name='user_account/login.html', 
                form_class=UserLoginForm
            ), 
            name='login'
        ),
    path('logout', 
            LogoutView.as_view(
                next_page='login/'
            ), 
            name='logout' 
        )
]