from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

class SigninTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)

    def test_signin_success(self):
        # Send POST request to /api/signin/
        response = self.client.post('/api/signin/', {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_signin_invalid_credentials(self):
        # Send POST request with invalid credentials
        response = self.client.post('/api/signin/', {'username': 'wronguser', 'password': 'wrongpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
class MeTests(APITestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)
        # Sign in and obtain token
        response = self.client.post('/api/signin/', {'username': self.username, 'password': self.password}, format='json')
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_me_authenticated(self):
        # Send GET request to /api/me/ with token
        response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.username)

    def test_me_unauthenticated(self):
        # Send GET request to /api/me/ without token
        self.client.credentials()  # Remove any authentication credentials
        response = self.client.get('/api/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)