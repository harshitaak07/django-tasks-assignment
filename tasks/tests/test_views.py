from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import datetime, timedelta
from tasks.models import Task

class TaskViewSetTest(APITestCase):
    def setUp(self):
        base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.task_1 = Task.objects.create(title="View Test", created_at=datetime.now() - timedelta(days=1))
        self.task_2 = Task.objects.create(title="New Task", created_at=datetime.now() - timedelta(days=2))
        self.task_3 = Task.objects.create(title="View New Task", created_at=datetime.now() - timedelta(days=3))

    def test_list_tasks(self):
        url = reverse("task-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("View Test", str(response.data))
        self.assertIn("New Task", str(response.data))

    def test_create_task(self):
        url = reverse("task-list")
        response = self.client.post(url, {"title": "Another Task"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_partial_update(self):
        url = reverse("task-detail", kwargs={"pk": self.task_1.id})
        response = self.client.patch(url, {"status": "Completed"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Completed")

    def test_delete_task(self):
        url = reverse("task-detail", kwargs={"pk": self.task_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_by_title(self):
        url = reverse("task-list") + "?search=New"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("New Task", str(response.data))
        self.assertIn("View New Task", str(response.data))

    def test_filter_by_date(self):
        url = reverse("task-list") + "?start_date=2023-09-01&end_date=2023-09-30"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("New Task", str(response.data))

    def test_sort_by_date_ascending(self):
        url = reverse("task-list") + "?sort_by_date=false"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task_titles = [task['title'] for task in response.data]
        self.assertEqual(task_titles, ["View Test", "New Task", "View New Task"])