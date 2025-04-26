import logging
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from tasks.models import Task

logger = logging.getLogger('django')

# Test class for Task ViewSet using DRF's APITestCase to test CRUD operations for Task model.
class TaskViewSetTest(APITestCase):
    # Set up test data for the Task model.
    def setUp(self):
        logger.info("Setting up test data")
        base_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.task_1 = Task.objects.create(title="View Test", created_at=timezone.now() - timedelta(days=1))
        self.task_2 = Task.objects.create(title="New Task", created_at=timezone.now() - timedelta(days=2))
        self.task_3 = Task.objects.create(title="View New Task", created_at=timezone.now() - timedelta(days=3))
        logger.info(f"Created tasks: {self.task_1.title}, {self.task_2.title}, {self.task_3.title}")

    # Test the listing of tasks.
    def test_list_tasks(self):
        logger.info("Running test_list_tasks")
        url = reverse("task-list")  # URL for the task list endpoint
        response = self.client.get(url)
        logger.info(f"Response status: {response.status_code}, response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("View Test", str(response.data))
        self.assertIn("New Task", str(response.data))

    # Test creating a new task.
    def test_create_task(self):
        logger.info("Running test_create_task")
        url = reverse("task-list")  
        data = {"title": "Another Task"}
        logger.info(f"Posting data: {data}")
        response = self.client.post(url, data)
        logger.info(f"Response status: {response.status_code}, response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    # Test partially updating an existing task.
    def test_partial_update(self):
        logger.info("Running test_partial_update")
        url = reverse("task-detail", kwargs={"pk": self.task_1.id}) # URL for task details with pk
        data = {"status": "Completed"}  
        logger.info(f"Patching task {self.task_1.id} with data: {data}")
        response = self.client.patch(url, data)
        logger.info(f"Response status: {response.status_code}, response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Completed")


    # Test deleting an existing task.
    def test_delete_task(self):
        logger.info("Running test_delete_task")
        url = reverse("task-detail", kwargs={"pk": self.task_1.id})  # URL for task details with pk
        logger.info(f"Deleting task {self.task_1.id}")
        response = self.client.delete(url)
        logger.info(f"Response status: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    # Test searching tasks by title.
    def test_search_by_title(self):
        logger.info("Running test_search_by_title")
        url = reverse("task-list") + "?search=New"  # Search query for title containing 'New'
        logger.info(f"Sending GET request to URL: {url}")
        response = self.client.get(url)
        logger.info(f"Response status: {response.status_code}, response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("New Task", str(response.data))
        self.assertIn("View New Task", str(response.data))


    # Test filtering tasks by a date range.
    def test_filter_by_date(self):
        logger.info("Running test_filter_by_date")
        url = reverse("task-list") + "?start_date=2023-09-01&end_date=2023-09-30"  # Filter tasks by date range
        logger.info(f"Sending GET request to URL: {url}")
        response = self.client.get(url)
        logger.info(f"Response status: {response.status_code}, response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("New Task", str(response.data))


    # Test sorting tasks by date in ascending order.
    def test_sort_by_date_ascending(self):
        logger.info("Running test_sort_by_date_ascending")
        url = reverse("task-list") + "?sort_by_date=false"  # Sort tasks by date (ascending)
        logger.info(f"Sending GET request to URL: {url}")
        response = self.client.get(url)
        logger.info(f"Response status: {response.status_code}, response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task_titles = [task['title'] for task in response.data['results']]  # Access the tasks in 'results' key
        logger.info(f"Sorted task titles: {task_titles}")
        self.assertEqual(task_titles, ["View Test", "New Task", "View New Task"])  # Verify the order of titles
