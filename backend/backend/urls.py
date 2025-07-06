from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('comptes.urls')),       # endpoints d'authentification
    path('api/',  include('location_api.urls')),  # endpoints métiers
]

# Servir les fichiers uploadés uniquement en développement
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
