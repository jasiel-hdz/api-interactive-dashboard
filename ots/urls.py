from django.urls import path
from .views import OTSListView

urlpatterns = [
    path('ots/', OTSListView.as_view(), name='ots-list'),
]