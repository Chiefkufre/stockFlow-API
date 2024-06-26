from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, SupplierItemViewSet

router = DefaultRouter()
router.register(r"items", ItemViewSet)

""" I created this route for testing purposes but you can uncomment
    if you intend to interest with the SupplierItem class
    All wrote will appear on swagger after you uncomment this
"""
# router.register(r"items-supplier", SupplierItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
