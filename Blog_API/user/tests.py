from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserRegistrationTest(APITestCase):
    """
    Test case for user registration.
    This test case verifies that a user can successfully register by sending a POST request
    to the registration endpoint with the required user details. It checks that the response
    status code is 201 (Created), the response message indicates successful user creation,
    and that the user is actually created in the database.
    Methods:
        test_register_user: Tests user registration functionality.
    """
    
    def test_register_user(self):
        url = reverse('register')  # Ensure this matches your URL name
        data = {
            "email": "johndoe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "securepassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully.')
        self.assertTrue(User.objects.filter(email="johndoe@example.com").exists())


class UserLoginTest(APITestCase):
    """
    Tests for user login functionality.
    Classes:
        UserLoginTest: Test case for user login.
    Methods:
        setUp(self): Sets up a test user for login tests.
        test_login_user(self): Tests that a user can log in with valid credentials.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            email="johndoe@example.com",
            first_name="John",
            last_name="Doe",
            password="securepassword123"
        )

    def test_login_user(self):
        url = reverse('login')  # Ensure this matches your URL name
        data = {
            "email": "johndoe@example.com",
            "password": "securepassword123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Login successful.')
        self.assertIn('access_token', response.data)


class LogoutViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        self.logout_url = reverse('logout')  # Ensure you have a URL pattern named 'logout'

    def test_logout_successful(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.logout_url, {'refresh_token': self.refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logout successful.')

    def test_logout_no_refresh_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Refresh token not provided.')

    def test_logout_invalid_refresh_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.post(self.logout_url, {'refresh_token': 'invalidtoken'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid or expired refresh token.')
