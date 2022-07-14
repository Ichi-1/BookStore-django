from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('a098c8d9c3c6c6ac2ede4a4eb2ed/', admin.site.urls),
    path('', include('apps.store.urls', namespace='store')),
    path('basket/', include('apps.basket.urls', namespace='basket')),
    path('account/', include('apps.account.urls', namespace='account')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('checkout/', include('apps.checkout.urls', namespace='checkout')),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
