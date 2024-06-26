from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="StockFlow",
        default_version="1.0.0",
        description="API documentation for Inventory and Supplier management system",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="samuel@stockflow.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)
