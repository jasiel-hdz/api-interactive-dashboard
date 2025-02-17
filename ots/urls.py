from django.urls import path
from .views import OTSDayView, OTSWeekView

urlpatterns = [
    path('day', OTSDayView.as_view(), name='ots-list-day'),
    path('week', OTSWeekView.as_view(), name='ots-list-week'),
]