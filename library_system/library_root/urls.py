# library_system/library_root/urls.py



from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # For login/signup
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),  # Include dashboard URLs with namespace
]