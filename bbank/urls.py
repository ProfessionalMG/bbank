from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('wallet.urls')),
    path('api/', include('wallet.api.urls')),
]
