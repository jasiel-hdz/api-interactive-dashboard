from django.contrib import admin
from django.urls import path

# from taskmanager.views import TaskListAPIView, TaskDetailAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('tasks/', TaskListAPIView.as_view(), name='task-list'),
    # path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    # path('api-auth/', include('rest_framework.urls')),
]
