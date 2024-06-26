from rest_framework import viewsets
from .models import Item, SupplierItem
from .serializers import ItemSerializer, SupplierItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class SupplierItemViewSet(viewsets.ModelViewSet):
    queryset = SupplierItem.objects.all()
    serializer_class = SupplierItemSerializer

    def partial_update(self, request, *args, **kwargs):
        # This method will us to perform oartial update on the api
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)
