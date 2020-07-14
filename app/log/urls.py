from django.urls import path
from log import views


app_name = 'log'

urlpatterns = [
    # rotas protegidas somente para usuários com conta visualizarem
    path('logs/results', views.SearchLogsView.as_view(), name='search_logs'),
    path('logs/', views.ListLogsView.as_view(), name='all_logs'),
    path('logs/<int:pk>', views.SingleLogView.as_view(), name='single_log'),
]
