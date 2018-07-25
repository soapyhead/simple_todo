from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from companies.models import Company
from .models import Todo
import json


class TodosTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user_data = {
            'email': 'todotester@test.ru',
            'password': '123qwe123',
            'companies': ['todo_test1', 'todo_test2']
        }
        user = get_user_model().objects.create_user_with_companies(**user_data)
        cls.client_user = user
        cls.token = Token.objects.create(user=cls.client_user)

        todos = [
            Todo(
                description='todo test1 1',
                completed=False,
                company=Company.objects.get(name='todo_test1')
            ),
            Todo(
                description='todo test1 2',
                completed=False,
                company=Company.objects.get(name='todo_test1')
            ),
            Todo(
                description='todo test1 3',
                completed=False,
                company=Company.objects.get(name='todo_test1')
            ),
            Todo(
                description='todo test1 4',
                completed=True,
                company=Company.objects.get(name='todo_test1')
            ),
            Todo(
                description='todo test1 5',
                completed=True,
                company=Company.objects.get(name='todo_test1')
            ),
            Todo(
                description='todo test1 6',
                completed=False,
                company=Company.objects.get(name='todo_test1')
            ),
            Todo(
                description='todo test2 1',
                completed=False,
                company=Company.objects.get(name='todo_test2')
            ),
            Todo(
                description='todo test2 2',
                completed=False,
                company=Company.objects.get(name='todo_test2')
            ),
            Todo(
                description='todo test2 3',
                completed=True,
                company=Company.objects.get(name='todo_test2')
            ),
            Todo(
                description='todo test2 4',
                completed=False,
                company=Company.objects.get(name='todo_test2')
            )
        ]

        Todo.objects.bulk_create(todos)

    def test_login_with_company_1(self):
        url = reverse('login')
        data = {
            'email': 'todotester@test.ru',
            'password': '123qwe123',
            'auth_company': 'todo_test1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/todos/', format='json')
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 6)

    def test_login_with_company_2(self):
        url = reverse('login')
        data = {
            'email': 'todotester@test.ru',
            'password': '123qwe123',
            'auth_company': 'todo_test2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/todos/', format='json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 4)

    def test_create_todo(self):
        url = reverse('login')
        data = {
            'email': 'todotester@test.ru',
            'password': '123qwe123',
            'auth_company': 'todo_test1'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_todo = {'description': 'todo test1 7'}
        response = self.client.post('/api/todos/', new_todo, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/api/todos/', format='json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 7)

    def test_update_todo(self):
        url = reverse('login')
        data = {
            'email': 'todotester@test.ru',
            'password': '123qwe123',
            'auth_company': 'todo_test1'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/todos/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        patch_data = {'completed': True}
        response = self.client.patch('/api/todos/1/', patch_data, format='json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['completed'], True)

    def test_delete_todo(self):
        url = reverse('login')
        data = {
            'email': 'todotester@test.ru',
            'password': '123qwe123',
            'auth_company': 'todo_test1'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/todos/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete('/api/todos/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/api/todos/', format='json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 5)

    def test_permission_todo(self):
        url = reverse('login')
        # авторизуюсь под одной организацией
        data = {
            'email': 'todotester@test.ru',
            'password': '123qwe123',
            'auth_company': 'todo_test1'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/todos/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # авторизуюсь под другой организацией
        data = {
            'email': 'todotester@test.ru',
            'password': '123qwe123',
            'auth_company': 'todo_test2'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/todos/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)