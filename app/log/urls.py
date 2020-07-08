from django.urls import path
from log import views

urlpatterns = [
    path('logs/', views.ListLogsView.as_view(), name='log'),
    path('logs/<int:pk>', views.DetailLogView.as_view(), name='logs'),
]
