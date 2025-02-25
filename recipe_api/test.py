from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class ApiUrlTests(TestCase):
    def test_register(self):
        url = reverse('register')  # 'register' is the name of the URL pattern
        response = self.client.post(url, data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('login')
        response = self.client.post(url, data={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_details(self):
        url = reverse('update-user-details')
        response = self.client.put(url, data={
            'email': 'newemail@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile(self):
        url = reverse('user-profile', args=[1])  # Assuming user ID 1 exists
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_generate_response(self):
        url = reverse('generate_response')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_saved_recipes(self):
        url = reverse('saved_recipe_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
