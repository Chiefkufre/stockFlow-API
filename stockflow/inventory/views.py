from rest_framework import viewsets
from .models import ImageUrl, Item, Product, SupplierItem
from .serializers import ImageUrlSerializer, ItemSerializer, ProductSerializer, SupplierItemSerializer


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

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ImageUrlViewSet(viewsets.ModelViewSet):
    queryset = ImageUrl.objects.all()
    serializer_class = ImageUrlSerializer