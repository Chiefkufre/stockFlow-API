from django.core.exceptions import ObjectDoesNotExist
from django.http import response
from rest_framework import serializers
from .models import Item, SupplierItem
from .models import Product, ImageUrl
from supplier.models import Supplier


class SupplierItemSerializer(serializers.ModelSerializer):
    supplier_name = serializers.ReadOnlyField(source="supplier.name")
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), source="supplier"
    )

    class Meta:
        model = SupplierItem
        fields = [
            "id",
            "supplier_id",
            "item",
            "quantity",
            "supply_date",
            "supplier_name",
        ]


class ItemSerializer(serializers.ModelSerializer):
    # suppliers = SupplierItemSerializer(many=True, write_only=True)
    quantity = serializers.ReadOnlyField()
    supplier_data = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField()),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "date_added",
            "suppliers",
            "supplier_data",
        ]
    def create(self, validated_data):
        supplier_data = validated_data.pop("supplier_data", [])
        item = super().create(validated_data)
        self._create_supplier_items(item, supplier_data)
        return item

    def update(self, instance, validated_data):
        supplier_data = validated_data.get("supplier_data", None)

        if supplier_data is not None:

            # This allow me to verify the suppliers id
            supplier_ids = [data["supplier_id"] for data in supplier_data]
            existing_suppliers = Supplier.objects.filter(id__in=supplier_ids)
            existing_supplier_ids = set(existing_suppliers.values_list("id", flat=True))

            # This section allows us to verify if IDs arre valid to protect
            # the system from failing when an unknown supplier ID is used
            for supplier_id in supplier_ids:
                if supplier_id not in existing_supplier_ids:
                    raise serializers.ValidationError(
                        {"error": f"Supplier with ID {supplier_id} does not exist."}
                    )

            for _data in supplier_data:
                supplier_id = _data.get("supplier_id")
                quantity = _data.get("quantity")

                existing_item = instance.supplier_items.filter(
                    supplier_id=supplier_id
                ).first()

                if existing_item:
                    existing_item.quantity = quantity
                    existing_item.save()
                else:
                    SupplierItem.objects.create(
                        item=instance, supplier_id=supplier_id, quantity=quantity
                    )

            # Update total quantity based on all supplier items
            total_quantity = sum(
                item.quantity for item in instance.supplier_items.all()
            )
            instance.quantity = total_quantity

        # Update the rest of the instance fields
        instance = super().update(instance, validated_data)
        instance.save()

        return instance

    def _create_supplier_items(self, item, supplier_data):
        """This method bind each item to each supplier and add
            their quantities per supplier
        """
        supplier_items = [
            SupplierItem(item=item, supplier_id=data["supplier_id"], quantity=data["quantity"])
            for data in supplier_data
        ]
        SupplierItem.objects.bulk_create(supplier_items)

    

class ImageUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUrl
        fields = ['thumbnail', 'mobile', 'tablet', 'desktop']

class ProductSerializer(serializers.ModelSerializer):
    imgUrl = ImageUrlSerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'imgUrl']

    def create(self, validated_data):
        img_url_data = validated_data.pop('imgUrl')
        img_url = ImageUrl.objects.create(**img_url_data)
        product = Product.objects.create(imgUrl=img_url, **validated_data)
        return product
