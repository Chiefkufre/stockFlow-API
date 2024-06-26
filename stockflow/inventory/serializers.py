from django.core.exceptions import ObjectDoesNotExist
from django.http import response
from rest_framework import serializers
from .models import Item, SupplierItem
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
        # We use pop here to detach ther supplier_data from the
        # validated_data since it is not required to create item
        supplier_data = validated_data.pop("supplier_data", [])
        item = super().create(validated_data)
        total_quantity = 0
        for supplier_data in supplier_data:
            supplier_id = supplier_data.get("supplier_id")
            quantity = supplier_data.get("quantity")

            # After creating the record of each item, we bind the item
            # to the suppliers and also specify their quantity
            # With, we can keep track of suppliers vs item relationship
            SupplierItem.objects.create(
                item=item, supplier_id=supplier_id, quantity=quantity
            )
            total_quantity += quantity

        """The total quantity of each item should ideally be equal to the quantity
            supply the by suppliers. This will allow us to automatically calculate 
            from the suppliers data. See the supplierItem model for the quantity
        """
        item.quantity = total_quantity
        item.save()
        return item

    def update(self, instance, validated_data):
        supplier_data = validated_data.get("supplier_data", None)

        if supplier_data is not None:
            # Check if all supplier IDs exist
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
