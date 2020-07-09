from django.urls import path
from log import views

urlpatterns = [
    path('logs/', views.SearchLogsView.as_view(), name='search'),
    path('logs/', views.ListLogsView.as_view(), name='logs'),
    path('logs/<int:pk>', views.DetailLogView.as_view(), name='log'),
]
