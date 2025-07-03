from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductoViewSet, ReseñaViewSet  # 👈 incluimos ReseñaViewSet

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'resenas', ReseñaViewSet)  # 👈 nueva ruta para reseñas

urlpatterns = [
    path('', include(router.urls)),
]
