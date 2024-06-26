from django.db import models
from supplier.models import Supplier


class Item(models.Model):
    """The models repr items in the inventory
        Each item relates to the supplier through
        a many2many relationship
    
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    suppliers = models.ManyToManyField(
        Supplier, related_name="item", through="SupplierItem"
    )

    def __str__(self):
        return self.name


class SupplierItem(models.Model):
    """The models allows us to connect the inventory
        to suppliers. When Items are add to db, this model
        is automatically populated
    
    """
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE, related_name="supplier_items"
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    supply_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("item", "supplier")
