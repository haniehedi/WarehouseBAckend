from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Warehouse, Ware, Factor

User = get_user_model()

class WarehouseAPITest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', role='admin')
        self.staff_user = User.objects.create_user(username='staff', password='staffpass', role='staff')
        self.regular_user = User.objects.create_user(username='user', password='userpass', role='user')

        self.warehouse = Warehouse.objects.create(user=self.admin_user, name='Admin Warehouse')
        self.ware = Ware.objects.create(
            user=self.admin_user,
            warehouse=self.warehouse,
            cost_method=Ware.weighted_mean,
            name='Admin Ware'
        )

        self.factor = Factor.objects.create(
            user=self.admin_user,
            ware=self.ware,
            quantity=5,
            purchase_price=10.00,
            type='input',
            total_cost=50.00
        )

    def test_admin_can_create_warehouse(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('warehouses-list'), {'name': 'New Warehouse'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_staff_can_create_warehouse(self):
        self.client.login(username='staff', password='staffpass')
        response = self.client.post(reverse('warehouses-list'), {'name': 'Staff Warehouse'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_cannot_create_warehouse(self):
        self.client.login(username='user', password='userpass')
        response = self.client.post(reverse('warehouses-list'), {'name': 'User Warehouse'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_view_all_warehouses(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('warehouses-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_staff_can_view_own_warehouses(self):
        self.client.login(username='staff', password='staffpass')
        response = self.client.get(reverse('warehouses-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No warehouses created by staff

    def test_user_can_view_all_warehouses(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('warehouses-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_view_all_wares(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('wares-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_staff_can_view_own_wares(self):
        self.client.login(username='staff', password='staffpass')
        response = self.client.get(reverse('wares-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No wares created by staff

    def test_user_can_view_all_wares(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('wares-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_warehouse(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.delete(reverse('warehouses-detail', args=[self.warehouse.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_staff_cannot_delete_other_users_warehouses(self):
        self.client.login(username='staff', password='staffpass')
        response = self.client.delete(reverse('warehouses-detail', args=[self.warehouse.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_factor_creation_by_admin(self):
        self.client.login(username='admin', password='adminpass')
        data = {
            'ware': self.ware.id,
            'quantity': 3,
            'purchase_price': 30.00,
            'type': 'input'
        }
        response = self.client.post(reverse('factors-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_factor_creation_by_staff(self):
        self.client.login(username='staff', password='staffpass')
        data = {
            'ware': self.ware.id,
            'quantity': 2,
            'purchase_price': 20.00,
            'type': 'input'
        }
        response = self.client.post(reverse('factors-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_factor_creation_by_regular_user(self):
        self.client.login(username='user', password='userpass')
        data = {
            'ware': self.ware.id,
            'quantity': 1,
            'purchase_price': 10.00,
            'type': 'input'
        }
        response = self.client.post(reverse('factors-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
