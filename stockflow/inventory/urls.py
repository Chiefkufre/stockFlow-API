from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, ProductViewSet, SupplierItemViewSet

router = DefaultRouter()
router.register(r"items", ItemViewSet)
router.register(r'products', ProductViewSet)

""" I registered this routes for testing purposes but you can uncomment
    if you intend to interest with the SupplierItem class
    All wrote will appear on swagger after you uncomment this
"""
# router.register(r"items-supplier", SupplierItemViewSet)
# router.register(r'imageurls', ImageUrlViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
