from django.contrib import admin
from django.urls import path, include

url = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{url}ots/', include('ots.urls')),
    path(f'{url}viewers/', include('viewers.urls')),
]
