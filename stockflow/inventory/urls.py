from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, SupplierItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'supplier-items', SupplierItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
