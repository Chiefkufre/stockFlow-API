from django.db import models


class Supplier(models.Model):
    """Model for storing supplier information"""

    name = models.CharField(max_length=100)
    email = models.TextField()
    address = models.TextField()

    def __str__(self):
        return self.name
