from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from supplier.models import Supplier
from inventory.models import Item, SupplierItem

class SupplierAPITests(APITestCase):
    def setUp(self):
        self.supplier1 = Supplier.objects.create(name='Supplier 1', email='supplier1@example.com', address='Lagos. Nigeria')
        self.supplier2 = Supplier.objects.create(name='Supplier 2', email='supplier2@example.com', address='Lagos2. Nigeria')
        self.item1 = Item.objects.create(name='Item 1', description='Description 1', price=10.00)
        SupplierItem.objects.create(item=self.item1, supplier=self.supplier1, quantity=50)

    def test_create_supplier(self):
        url = reverse('supplier-list')
        data =  {
            "name": "Masuna",
            "email": "contact@masuna.com",
            "address": "Lagos Nigeria"
             } 

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 3)

    def test_retrieve_supplier(self):
        url = reverse('supplier-detail', args=[self.supplier1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.supplier1.name)

    def test_update_supplier(self):
        url = reverse('supplier-detail', args=[self.supplier1.id])
        data = {
            "name": "Updated Supplier 1",
            "email": "updated_supplier1@example.com",
            "address": "Nigeria"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.supplier1.refresh_from_db()
        self.assertEqual(self.supplier1.name, "Updated Supplier 1")
        self.assertEqual(self.supplier1.email, "updated_supplier1@example.com")

    def test_partial_update_supplier(self):
        url = reverse('supplier-detail', args=[self.supplier1.id])
        data = {"address": "Nigeria"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.supplier1.refresh_from_db()
        self.assertEqual(self.supplier1.address, "Nigeria")

    def test_delete_supplier(self):
        url = reverse('supplier-detail', args=[self.supplier1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Supplier.objects.count(), 1)
        self.assertEqual(SupplierItem.objects.filter(supplier=self.supplier1).count(), 0)
