from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import datetime, timedelta
from tasks.models import Task, TaskStatus

class TaskIntegrationTest(APITestCase):
    def setUp(self):
        now = datetime.now()
        self.task1 = Task.objects.create(
            title="Read Book",
            description="Read a sci-fi novel",
            status=TaskStatus.PENDING,
            due_date=now + timedelta(days=5),
            priority=1,
            created_at=now - timedelta(days=3)
        )
        self.task2 = Task.objects.create(
            title="Write Report",
            description="Weekly report",
            status=TaskStatus.COMPLETED,
            due_date=now + timedelta(days=2),
            priority=2,
            created_at=now - timedelta(days=2)
        )
        self.task3 = Task.objects.create(
            title="Read Docs",
            description="API documentation",
            status=TaskStatus.PENDING,
            due_date=now + timedelta(days=1),
            priority=3,
            created_at=now - timedelta(days=1)
        )

    def test_list_tasks(self):
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_task(self):
        url = reverse('task-list')
        payload = {
            "title": "New Task",
            "description": "Description of new task",
            "status": TaskStatus.PENDING,
            "priority": 0
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Task")

    def test_partial_update_status(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        response = self.client.patch(url, {"status": TaskStatus.COMPLETED})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], TaskStatus.COMPLETED)

    def test_delete_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_search_by_title(self):
        url = reverse('task-list') + "?search=Read"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Read" in task['title'] for task in response.data))

    def test_filter_by_exact_created_date(self):
        search_date = (self.task2.created_at).strftime("%Y-%m-%d")
        url = reverse('task-list') + f"?search_date={search_date}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(task['id'] == self.task2.id for task in response.data))

    def test_sort_by_created_date_ascending(self):
        url = reverse('task-list') + "?sort_by_date=false"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [task['title'] for task in response.data]
        expected = [self.task1.title, self.task2.title, self.task3.title]
        self.assertEqual(titles, expected)

    def test_sort_by_created_date_descending(self):
        url = reverse('task-list') + "?sort_by_date=true"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [task['title'] for task in response.data]
        expected = [self.task3.title, self.task2.title, self.task1.title]
        self.assertEqual(titles, expected)

    def test_invalid_search_date_format(self):
        url = reverse('task-list') + "?search_date=invalid-date"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)