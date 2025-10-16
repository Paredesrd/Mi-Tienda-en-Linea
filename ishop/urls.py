from django.contrib import admin
from django.urls import path, include

# Importaciones necesarias para servir archivos de medios
from django.conf import settings
from django.conf.urls.static import static

from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.base, name='base'),
    path('', include('store.urls')),
    # La línea conflictiva del carrito ha sido eliminada de aquí.
]

# Añadir esta línea al final para servir archivos de medios en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)