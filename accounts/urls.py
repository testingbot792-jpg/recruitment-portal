from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('signup/', views.signup),
    path('login/', views.login_view),
    path('dashboard/', views.dashboard),
    path('logout/', views.logout_view),
    path('candidate-dashboard/', views.candidate_dashboard),
    path('upload-resume/', views.upload_resume),
    path('delete-resume/', views.delete_resume),
    path('resume/<str:user_id>/', views.view_resume),
    path('candidates/', views.candidate_list),
    path('profile/', views.profile),
]