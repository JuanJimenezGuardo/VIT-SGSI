from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RiskViewSet

# Usamos DefaultRouter de DRF, que crea automáticamente las rutas para el CRUD 
# y también reconoce nuestros endpoints custom (@action)
router = DefaultRouter()
router.register(r'risks', RiskViewSet, basename='risk')

urlpatterns = [
    path('', include(router.urls)),
]