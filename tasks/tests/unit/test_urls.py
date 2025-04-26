from rest_framework.test import APITestCase
from rest_framework import status

class TaskViewSetTest(APITestCase):
    def setUp(self):
        self.url = '/tasks/'  # Endpoint URL
    def test_task_create(self):
        data = {
            'title': 'Test Task',
            'description': 'Test task description',
            'due_date': '2025-12-31',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
