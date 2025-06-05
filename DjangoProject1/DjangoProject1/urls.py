from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('consumo/', include('consumo.urls')),
    path('', lambda request: redirect('test_view')),  # redirige a /consumo/test/
]
