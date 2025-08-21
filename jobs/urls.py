from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.job_list, name='job_list'),
    path('create/', views.job_create, name='job_create'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/update/', views.job_update, name='job_update'),
    path('<int:job_id>/delete/', views.job_delete, name='job_delete'),
]