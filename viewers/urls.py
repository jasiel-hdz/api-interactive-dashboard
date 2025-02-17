from django.urls import path
from .views import ViewersDayView, ViewersWeekView

urlpatterns = [
    path('day', ViewersDayView.as_view(), name='viewers-list-day'),
    path('week', ViewersWeekView.as_view(), name='viewers-list-week'),
]