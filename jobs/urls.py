from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list),
    path('add/', views.add_job),
    path('apply/<job_id>/', views.apply_job),
]