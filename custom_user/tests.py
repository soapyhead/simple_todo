from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from companies.models import Company


class AccountsTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        data = {
            'email': 'tester@test.ru',
            'password': '123qwe123',
            'companies': ['test1', 'test2']
        }
        user = get_user_model().objects.create_user_with_companies(**data)
        cls.client_user = user
        cls.token = Token.objects.create(user=cls.client_user)

    def test_sign_up(self):
        url = reverse('sign_up')
        data = {
            'email': 'tester1@test.ru',
            'password': '123qwe123',
            'companies': ['casino777', 'apple']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.all().count(), 4)

    def test_login(self):
        url = reverse('login')
        data = {
            'email': 'tester@test.ru',
            'password': '123qwe123',
            'auth_company': 'test1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_upper_email(self):
        url = reverse('login')
        data = {
            'email': 'TESTER@TEST.RU',
            'password': '123qwe123',
            'auth_company': 'test1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_up_with_no_password(self):
        url = reverse('sign_up')
        data = {
            'email': 'foo@example.com',
            'password': '',
            'companies': ['casino777']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_with_no_companies(self):
        url = reverse('sign_up')
        data = {
            'email': 'foo@example.com',
            'password': '',
            'companies': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_no_password(self):
        url = reverse('login')
        data = {
            'email': 'tester@test.ru',
            'password': '',
            'auth_company': 'test1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_no_company(self):
        url = reverse('login')
        data = {
            'email': 'tester@test.ru',
            'password': '123qwe123',
            'auth_company': ''
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
