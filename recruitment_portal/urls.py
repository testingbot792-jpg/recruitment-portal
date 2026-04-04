from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # ✅ Django admin

    path('', include('accounts.urls')),   # login, signup, dashboard
    path('jobs/', include('jobs.urls')), # jobs module
]