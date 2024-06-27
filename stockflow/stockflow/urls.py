
from django.contrib import admin
from django.urls import path, include
from .swagger import schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/inventory/', include('inventory.urls')),
    path('api/supplier/', include('supplier.urls')),
    path('/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
