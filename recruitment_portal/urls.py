from django.urls import path, include

urlpatterns = [
    path('', include('accounts.urls')),
    path('jobs/', include('jobs.urls')),
]