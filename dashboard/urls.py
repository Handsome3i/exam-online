from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('exam/<int:exam_id>/', views.exam_stats, name='exam_stats'),
    path('exam/<int:exam_id>/export/', views.export_scores, name='export_scores'),
]
