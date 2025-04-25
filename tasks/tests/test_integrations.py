import logging
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from tasks.models import Task, TaskStatus

logger = logging.getLogger('django')

class TaskIntegrationTest(APITestCase):
    def setUp(self):
        logger.info("Setting up test data for integration tests")
        now = timezone.now()
        self.task1 = Task.objects.create(
            title="Read The Book Dune",
            description="A classic sci-fi novel",
            status=TaskStatus.PENDING,
            due_date=now + timedelta(days=5),
            priority=1,
            created_at=now - timedelta(days=3)
        )
        self.task2 = Task.objects.create(
            title="Write Book Review",
            description="Write a Review of the Book Dune",
            status=TaskStatus.COMPLETED,
            due_date=now + timedelta(days=2),
            priority=2,
            created_at=now - timedelta(days=2)
        )
        self.task3 = Task.objects.create(
            title="Finish Python Project",
            description="Add Documentation to the Python Project",
            status=TaskStatus.PENDING,
            due_date=now + timedelta(days=1),
            priority=3,
            created_at=now - timedelta(days=1)
        )
        logger.info("Test data setup for integration tests complete")

    def test_list_tasks(self):
        logger.info("Running test_list_tasks to verify all tasks are present")
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        logger.info("Test list tasks passed - Total tasks found: %(task_count)s", {'task_count': len(response.data)})

    def test_create_task(self):
        logger.info("Running test_create_task to verify task creation")
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
        logger.info("Task created successfully - ID: %(task_id)s, Title: %(title)s", {
            'task_id': response.data['id'],
            'title': response.data['title']
        })

    def test_partial_update_status(self):
        logger.info(f"Running test_partial_update_status for task {self.task1.id} to verify partial update")
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        response = self.client.patch(url, {"status": TaskStatus.COMPLETED})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], TaskStatus.COMPLETED)
        logger.info("Task status updated successfully - ID: %(task_id)s, New status: %(status)s", {
            'task_id': self.task1.id,
            'status': response.data['status']
        })

    def test_delete_task(self):
        logger.info(f"Running test_delete_task for task {self.task1.id} to verify deletion")
        url = reverse('task-detail', kwargs={'pk': self.task1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())
        logger.info("Task deleted successfully - ID: %(task_id)s", {'task_id': self.task1.id})

    def test_search_by_title(self):
        logger.info("Running test_search_by_title to verify fuzzy search by title")
        url = reverse('task-list') + "?search=Read"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Read" in task['title'] for task in response.data))
        logger.info("Search by title passed - Found title: %(title)s", {'title': 'Read'})

    def test_filter_by_exact_created_date(self):
        logger.info("Running test_filter_by_exact_created_date to verify exact date filter")
        search_date = (self.task2.created_at).strftime("%Y-%m-%d")
        url = reverse('task-list') + f"?search_date={search_date}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(task['id'] == self.task2.id for task in response.data))
        logger.info("Filter by exact created date passed - Filtered date: %(search_date)s", {'search_date': search_date})

    def test_sort_by_created_date_ascending(self):
        logger.info("Running test_sort_by_created_date_ascending to verify ascending date sort")
        url = reverse('task-list') + "?sort_by_date=false"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [task['title'] for task in response.data]
        expected = [self.task1.title, self.task2.title, self.task3.title]
        self.assertEqual(titles, expected)
        logger.info("Sort by created date ascending passed - Sorted titles: %(titles)s", {'titles': titles})

    def test_invalid_search_date_format(self):
        logger.info("Running test_invalid_search_date_format to verify invalid date format")
        url = reverse('task-list') + "?search_date=invalid-date"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        logger.warning("Invalid search date format passed - Search date: %(search_date)s", {'search_date': 'invalid-date'})