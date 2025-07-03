from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from productos.views import RegistroView, CustomTokenObtainPairView  # ✅ Importar vista personalizada

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de tu app
    path('api/', include('productos.urls')),

    # ✅ Usar vista personalizada del token (para incluir el username)
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Ruta personalizada para el registro
    path('api/registro/', RegistroView.as_view(), name='registro'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
