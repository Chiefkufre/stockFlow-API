from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from inventory.models import Item, SupplierItem
from supplier.models import Supplier

class InventoryAPITests(APITestCase):
    def setUp(self):
        self.supplier1 = Supplier.objects.create(name='Supplier 1', email='supplier1@example.com', address='Lagos. Nigeria')
        self.supplier2 = Supplier.objects.create(name='Supplier 2', email='supplier2@example.com', address='Port Harcourt, Nigeria')
        self.item1 = Item.objects.create(name='Item 1', description='Description 1', price=10.00) 
        self.item2 = Item.objects.create(name='Item 2', description='Description 2', price=20.00)
        SupplierItem.objects.create(item=self.item1, supplier=self.supplier1, quantity=50)
        SupplierItem.objects.create(item=self.item2, supplier=self.supplier2, quantity=30)

    def test_create_item(self):
        url = reverse('item-list')
        data = {
            "name": "New Item",
            "description": "New Description",
            "price": 15.00,
            "supplier_data": [
                {"supplier_id": self.supplier1.id, "quantity": 10},
                {"supplier_id": self.supplier2.id, "quantity": 20}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 3)
        self.assertEqual(SupplierItem.objects.count(), 4)

    def test_retrieve_item(self):
        url = reverse('item-detail', args=[self.item1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item1.name)

    def test_update_item(self):
        url = reverse('item-detail', args=[self.item1.id])
        data = {
            "name": "Updated Item 1",
            "description": "Updated Description 1",
            "price": 25.00,
            "supplier_data": [
                {"supplier_id": self.supplier2.id, "quantity": 40}
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.name, "Updated Item 1")
        self.assertEqual(self.item1.quantity, 90)

    def test_partial_update_item(self):
        url = reverse('item-detail', args=[self.item1.id])
        data = {"price": 18.00}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.price, 18.00)

    def test_delete_item(self):
        url = reverse('item-detail', args=[self.item1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(SupplierItem.objects.filter(item=self.item1).count(), 0)
