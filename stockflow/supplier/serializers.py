from rest_framework import serializers
from .models import Supplier
from inventory.models import SupplierItem


class SupplierSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = ["id", "name", "address", "email", "items"]

    def validate_email(self, value):
        """Validation to prevent double account creation"""
        request = self.context.get("request")
        # This is here we validate that this method is only tigger
        # on update
        if request and request.method in ("PUT", "PATCH"):
            supplier_id = self.instance.id
            if Supplier.objects.filter(email=value).exclude(id=supplier_id).exists():
                raise serializers.ValidationError(
                    "A supplier with this email already exists."
                )
        else:
            if Supplier.objects.filter(email=value).exists():
                raise serializers.ValidationError(
                    "A supplier with this email already exists."
                )
        return value

    def get_items(self, obj):
        supplier_items = SupplierItem.objects.filter(supplier=obj)
        return [
            {
                "item_id": supplier_item.item.id,
                "item_name": supplier_item.item.name,
                "quantity": supplier_item.quantity,
            }
            for supplier_item in supplier_items
        ]
