from rest_framework import viewsets
from .models import Item, SupplierItem
from .serializers import ItemSerializer, SupplierItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class SupplierItemViewSet(viewsets.ModelViewSet):
    queryset = SupplierItem.objects.all()
    serializer_class = SupplierItemSerializer
