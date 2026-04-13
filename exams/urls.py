from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('create/', views.exam_create, name='exam_create'),
    path('<int:exam_id>/edit/', views.exam_edit, name='exam_edit'),
    path('<int:exam_id>/delete/', views.exam_delete, name='exam_delete'),
    path('<int:exam_id>/publish/', views.exam_publish, name='exam_publish'),
    path('<int:exam_id>/start/', views.exam_start, name='exam_start'),
    path('<int:exam_id>/take/', views.exam_take, name='exam_take'),
    path('<int:exam_id>/submit/', views.exam_submit, name='exam_submit'),
    path('<int:exam_id>/result/', views.exam_result, name='exam_result'),
    path('<int:exam_id>/preview/', views.exam_preview, name='exam_preview'),
]
