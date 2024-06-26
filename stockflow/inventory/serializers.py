from rest_framework import serializers
from .models import Item, SupplierItem
from supplier.models import Supplier

class SupplierItemSerializer(serializers.ModelSerializer):
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    supplier_id = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), source='supplier')

    class Meta:
        model = SupplierItem
        fields = ['id', 'supplier_id', 'item', 'quantity', 'supply_date', 'supplier_name']

    
class ItemSerializer(serializers.ModelSerializer):
    # suppliers = SupplierItemSerializer(many=True, write_only=True)
    quantity = serializers.ReadOnlyField()
    supplier_data = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField()), write_only=True, required=False
    )
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'price', 'quantity', 'date_added', 'suppliers', 'supplier_data']

    def create(self, validated_data):
        supplier_data = validated_data.pop('supplier_data', [])
        item = super().create(validated_data)
        total_quantity = 0
        for supplier_data in supplier_data:
            supplier_id = supplier_data.get('supplier_id')
            quantity = supplier_data.get('quantity')
            SupplierItem.objects.create(item=item, supplier_id=supplier_id, quantity=quantity)
            total_quantity += quantity
        
        """The total quantity of each item should ideally be equal to the quantity
            supply the by suppliers. This will allow us to automatically calculate 
            from the suppliers data. See the supplierItem model for the quantity
        """
        item.quantity = total_quantity
        item.save()
        return item

    def update(self, instance, validated_data):
        supplier_data = validated_data.pop('supplier_data', [])
        instance = super().update(instance, validated_data)
        instance.supplier_items.all().delete()
        total_quantity = 0
        for _data in supplier_data:
            supplier_id = _data.get('supplier_id')
            quantity = _data.get('quantity')

            SupplierItem.objects.create(item=instance, supplier_id=supplier_id, quantity=quantity)

            # We update the total item quantity here which is the suum of all supplied items
            total_quantity += quantity
        instance.quantity = total_quantity
        instance.save()
        return instance
