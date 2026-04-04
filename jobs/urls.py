from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list),
    path('add/', views.add_job),
    path('apply/<str:job_id>/', views.apply_job),
    path('company/<str:company_name>/', views.company_jobs),
    path('save/<str:job_id>/', views.save_job_view),
    path('edit/<str:job_id>/', views.edit_job),
    path('delete/<str:job_id>/', views.delete_job),
    path('logo/<str:job_id>/', views.job_logo),
]