"""
URL configuration for codemind project.
"""
from django.contrib import admin
from django.urls import path, include
from snippets.views import api_root_view

urlpatterns = [
    # Interactive Root API Index
    path('', api_root_view, name='api-root'),
    
    # Core API Endpoints
    path('api/', include('snippets.urls', namespace='snippets')),
    path('api/auth/', include('authentication.urls', namespace='authentication')),
    
    # Django Administration
    path('admin/', admin.site.urls),
]
