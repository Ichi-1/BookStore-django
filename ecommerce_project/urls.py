from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.store.urls', namespace='store')),
    path('basket/', include('apps.basket.urls', namespace='basket')),
    path('account/', include('apps.account.urls', namespace='account')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('checkout/', include('apps.checkout.urls', namespace='checkout')),
    # path('__debug__/', include('debug_toolbar.urls')),
]



if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )