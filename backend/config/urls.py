from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from .views import home

# Importar ViewSets
from apps.users.views import UserViewSet, AuditLogViewSet
from apps.companies.views import CompanyViewSet
from apps.projects.views import ProjectViewSet, ProjectUserViewSet
from apps.phases.views import PhaseViewSet
from apps.tasks.views import TaskViewSet

# Crear un único router compartido para evitar conflictos
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'project-users', ProjectUserViewSet)
router.register(r'phases', PhaseViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', home, name='home'),  # Ruta raíz
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Todas las rutas del router
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT
]
