import logging
from django.test import TestCase
from tasks.models import Task, TaskStatus
from django.utils import timezone
from django.core.exceptions import ValidationError

logger = logging.getLogger('django')

class TaskModelTest(TestCase):
    def test_basemodel_fields(self):
        logger.info("Running test_basemodel_fields to verify base model fields")
        task = Task.objects.create(title="Base Model Test")
        logger.info(f"Created task with ID: {task.id}")

        self.assertIsNotNone(task.id)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)

        created_at = task.created_at
        task.title = "Updated Task Title"
        task.save()
        self.assertEqual(task.created_at, created_at)
        self.assertGreater(task.updated_at, created_at)

        logger.info(f"Updated task with ID: {task.id}, created_at: {created_at}, updated_at: {task.updated_at}")

    def test_status_choices(self):
        logger.info("Running test_status_choices to verify status choices")
        choices = TaskStatus.choices()
        logger.info(f"TaskStatus choices for Task: {choices}")
        self.assertIn((TaskStatus.PENDING, 'Pending'), choices)

    def test_task_str(self):
        logger.info("Running test_task_str to verify task string representation")
        task = Task.objects.create(title="Test Task")
        logger.info(f"Created task with title: {task.title}")
        self.assertEqual(str(task), "Test Task (Pending)")

    def test_status_default(self):
        logger.info("Running test_status_default to verify default status")
        task = Task.objects.create(title="Default Status")
        logger.info(f"Created task with title: {task.title}, default status: {task.status}")
        self.assertEqual(task.status, TaskStatus.PENDING)

    def test_due_date_nullable_and_saves(self):
        logger.info("Running test_due_date_nullable_and_saves to verify due date")
        task = Task.objects.create(title="Deadline")
        logger.info(f"Created task with title: {task.title}, due_date: {task.due_date}")
        self.assertIsNone(task.due_date)

        now = timezone.now()
        task.due_date = now
        task.save()
        self.assertEqual(task.due_date, now)

        logger.info(f"Updated task with title: {task.title}, new due_date: {task.due_date}")

    def test_priority_field_default_and_custom(self):
        logger.info("Running test_priority_field_default_and_custom to verify priority field")
        task1 = Task.objects.create(title="Low")
        task2 = Task.objects.create(title="High", priority=10)
        logger.info(f"Created task1 with title: {task1.title}, priority: {task1.priority}")
        logger.info(f"Created task2 with title: {task2.title}, priority: {task2.priority}")
        
        self.assertEqual(task1.priority, 0)
        self.assertEqual(task2.priority, 10)

    def test_priority_field_invalid(self):
        logger.info("Running test_priority_field_invalid to verify invalid priority")
        task = Task.objects.create(title="Invalid Priority", priority=-1)
        logger.warning(f"Created task with invalid priority: {task.priority}")

        self.assertEqual(task.priority, -1)

        task = Task.objects.create(title="Very High Priority", priority=100)
        logger.info(f"Created task with priority: {task.priority}")
        self.assertEqual(task.priority, 100)

    def test_task_with_all_fields(self):
        logger.info("Running test_task_with_all_fields to verify all fields")
        from datetime import datetime
        now = timezone.now()
        task = Task.objects.create(
            title="Test Task",
            description="This is a test",
            status=TaskStatus.COMPLETED,
            due_date=now,
            priority=5
        )
        logger.info(f"Created task with title: {task.title}, status: {task.status}, due_date: {task.due_date}, priority: {task.priority}")
        
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test")
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertEqual(task.due_date, now)
        self.assertEqual(task.priority, 5)

    def test_title_not_null(self):
        logger.info("Running test_title_not_null to verify title not null")
        task = Task(title=None)
        logger.error("Attempted to create task with null title")
        with self.assertRaises(ValidationError):
            task.full_clean()