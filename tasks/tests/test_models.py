from django.test import TestCase
from tasks.models import Task, TaskStatus
from django.utils import timezone
from django.core.exceptions import ValidationError

class TaskModelTest(TestCase):
    def test_basemodel_fields(self):
        task = Task.objects.create(title="Base test")
        self.assertIsNotNone(task.id)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)

        created_at = task.created_at
        task.title = "Updated"
        task.save()
        self.assertEqual(task.created_at, created_at)
        self.assertGreater(task.updated_at, created_at)
    
    def test_status_choices(self):
        choices = TaskStatus.choices()
        self.assertIn((TaskStatus.PENDING, 'Pending'), choices)

    def test_task_str(self):
        task = Task.objects.create(title="Test Task")
        self.assertEqual(str(task), "Test Task (Pending)")

    def test_status_default(self):
        task = Task.objects.create(title="Default Status")
        self.assertEqual(task.status, TaskStatus.PENDING)
    
    def test_due_date_nullable_and_saves(self):
        task = Task.objects.create(title="Deadline")
        self.assertIsNone(task.due_date)

        from datetime import datetime
        now = timezone.now() 
        task.due_date = now
        task.save()
        self.assertEqual(task.due_date, now)
    
    def test_priority_field_default_and_custom(self):
        task1 = Task.objects.create(title="Low")
        task2 = Task.objects.create(title="High", priority=10)
        self.assertEqual(task1.priority, 0)
        self.assertEqual(task2.priority, 10)
    
    def test_priority_field_invalid(self):
        task = Task.objects.create(title="Invalid Priority", priority=-1)
        self.assertEqual(task.priority, -1)

        task = Task.objects.create(title="Very High Priority", priority=100)
        self.assertEqual(task.priority, 100)
    
    def test_task_with_all_fields(self):
        from datetime import datetime
        now = timezone.now()
        task = Task.objects.create(
            title="Test Task",
            description="This is a test",
            status=TaskStatus.COMPLETED,
            due_date=now,
            priority=5
        )
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test")
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertEqual(task.due_date, now)
        self.assertEqual(task.priority, 5)
    
    def test_title_not_null(self):
        task = Task(title=None)
        with self.assertRaises(ValidationError):
            task.full_clean() 