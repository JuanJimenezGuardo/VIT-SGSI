from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home, name='home'),  # Ruta raíz
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),  # Enlace a las URLs de la app 'users'
    path('api/', include('apps.companies.urls')),  # Enlace a las URLs de la app 'company'
    path('api/', include('apps.projects.urls')),  # Enlace a las URLs de la app 'projects'
    path('api/', include('apps.phases.urls')),  # Enlace a las URLs de la app 'phases'
    path('api/', include('apps.tasks.urls')),  # Enlace a las URLs de la app 'tasks'
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT - activar después
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT - activar después
]
