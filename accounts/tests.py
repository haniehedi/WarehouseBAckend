from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
        self.token_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.register_url = reverse('register')
        self.user_url = reverse('user_profile')

    def test_registration(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)

    def test_login(self):
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_retrieve_update_profile(self):
        # Obtain JWT token
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

        # Retrieve Profile
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

        # Update Profile - Email
        response = self.client.put(self.user_url, {'email': 'new@test.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'new@test.com')

        # Update Profile - Username
        response = self.client.put(self.user_url, {'username': 'newusername'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'newusername')
