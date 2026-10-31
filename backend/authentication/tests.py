import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationAPITests(APITestCase):
    """
    Test suite for CodeMind Vault Authentication endpoints.
    """

    def setUp(self):
        self.register_url = reverse('authentication:register')
        self.token_url = reverse('authentication:token_obtain_pair')
        self.token_refresh_url = reverse('authentication:token_refresh')
        self.me_url = reverse('authentication:current_user')
        
        self.user_data = {
            'username': 'codemind_dev',
            'email': 'dev@codemind.io',
            'password': 'SecureVaultPassword123!',
            'password_confirm': 'SecureVaultPassword123!'
        }

    def test_user_registration_success(self):
        """Verify registration creates user and returns JWT tokens."""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        self.assertEqual(response.data['user']['username'], 'codemind_dev')
        self.assertEqual(response.data['user']['email'], 'dev@codemind.io')

    def test_user_registration_password_mismatch(self):
        """Verify registration rejects mismatched passwords."""
        bad_data = self.user_data.copy()
        bad_data['password_confirm'] = 'DifferentPassword123!'
        response = self.client.post(self.register_url, bad_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_token_obtain_and_refresh(self):
        """Verify user can log in and refresh token."""
        # Create user
        User.objects.create_user(
            username='vault_user',
            email='vault@codemind.io',
            password='TestPassword123!'
        )

        # Obtain token
        login_data = {'username': 'vault_user', 'password': 'TestPassword123!'}
        login_res = self.client.post(self.token_url, login_data, format='json')
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_res.data)
        self.assertIn('refresh', login_res.data)

        access_token = login_res.data['access']
        refresh_token = login_res.data['refresh']

        # Access protected /api/auth/me/
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        me_res = self.client.get(self.me_url)
        self.assertEqual(me_res.status_code, status.HTTP_200_OK)
        self.assertEqual(me_res.data['username'], 'vault_user')

        # Refresh access token
        self.client.credentials()  # Clear auth header
        refresh_res = self.client.post(self.token_refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(refresh_res.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_res.data)
