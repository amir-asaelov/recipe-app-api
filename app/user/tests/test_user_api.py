"""
Tests for the user API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create and return a new User"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public feature of the User API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        # verify that http response code is 201 - created
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # retrieve a user from DB using the 'email'
        user = get_user_model().objects.get(email=payload['email'])

        # verify that the user 'password' match the hashed password in db
        self.assertTrue(user.check_password(payload['password']))

        # verify that the hashed user 'password' is not part of the response
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        # verify we got http 400 - failed to create the user
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        # verify we got http 400 - failed to create the user
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # check if user with 'email' exists (boolean) in the db
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        # 'user_exists' is expected to be false
        self.assertFalse(user_exists)
