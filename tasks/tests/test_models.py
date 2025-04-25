import logging
from django.test import TestCase
from tasks.models import Task, TaskStatus
from django.utils import timezone
from django.core.exceptions import ValidationError

# Setting up the logger for task-related operations
logger = logging.getLogger('django')

class TaskModelTest(TestCase):
    # Test for verifying base model fields (id, created_at, updated_at)
    def test_basemodel_fields(self):
        logger.info("Running test_basemodel_fields to verify base model fields")
        
        # Creating a task with a title
        task = Task.objects.create(title="Base Model Test")
        logger.info(f"Created task with ID: {task.id}")

        # Asserting that fields are not None
        self.assertIsNotNone(task.id)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)

        # Checking if created_at doesn't change upon update, and updated_at does
        created_at = task.created_at
        task.title = "Updated Task Title"
        task.save()
        self.assertEqual(task.created_at, created_at)
        self.assertGreater(task.updated_at, created_at)

        # Log the update details
        logger.info(f"Updated task with ID: {task.id}, created_at: {created_at}, updated_at: {task.updated_at}")

    # Test for checking if the TaskStatus choices are correct
    def test_status_choices(self):
        logger.info("Running test_status_choices to verify status choices")
        
        # Verifying that 'Pending' is one of the choices
        choices = TaskStatus.choices()
        logger.info(f"TaskStatus choices for Task: {choices}")
        self.assertIn((TaskStatus.PENDING, 'Pending'), choices)

    # Test for checking the string representation of a Task
    def test_task_str(self):
        logger.info("Running test_task_str to verify task string representation")
        
        # Creating a task with a title
        task = Task.objects.create(title="Test Task")
        logger.info(f"Created task with title: {task.title}")
        
        # Checking if the string representation of the task is as expected
        self.assertEqual(str(task), "Test Task (Pending)")

    # Test to verify if the default status for a task is 'Pending'
    def test_status_default(self):
        logger.info("Running test_status_default to verify default status")
        
        # Creating a task to check the default status
        task = Task.objects.create(title="Default Status")
        logger.info(f"Created task with title: {task.title}, default status: {task.status}")
        
        # Ensuring the default status is 'Pending'
        self.assertEqual(task.status, TaskStatus.PENDING)

    # Test to verify that the due date can be nullable and updated correctly
    def test_due_date_nullable_and_saves(self):
        logger.info("Running test_due_date_nullable_and_saves to verify due date")
        
        # Creating a task without a due date
        task = Task.objects.create(title="Deadline")
        logger.info(f"Created task with title: {task.title}, due_date: {task.due_date}")
        self.assertIsNone(task.due_date)

        # Adding and saving a due date
        now = timezone.now()
        task.due_date = now
        task.save()
        self.assertEqual(task.due_date, now)

        # Log the update details
        logger.info(f"Updated task with title: {task.title}, new due_date: {task.due_date}")

    # Test to verify the default and custom values for the priority field
    def test_priority_field_default_and_custom(self):
        logger.info("Running test_priority_field_default_and_custom to verify priority field")
        
        # Creating tasks with default and custom priority values
        task1 = Task.objects.create(title="Low")
        task2 = Task.objects.create(title="High", priority=10)
        
        # Logging the created tasks and their priorities
        logger.info(f"Created task1 with title: {task1.title}, priority: {task1.priority}")
        logger.info(f"Created task2 with title: {task2.title}, priority: {task2.priority}")
        
        # Verifying the priorities
        self.assertEqual(task1.priority, 0)  # Default priority should be 0
        self.assertEqual(task2.priority, 10)  # Custom priority should be 10

    # Test to verify invalid priority values
    def test_priority_field_invalid(self):
        logger.info("Running test_priority_field_invalid to verify invalid priority")
        
        # Creating tasks with invalid priorities and verifying their values
        task = Task.objects.create(title="Invalid Priority", priority=-1)
        logger.warning(f"Created task with invalid priority: {task.priority}")
        self.assertEqual(task.priority, -1)  # Invalid priority should still save
        
        task = Task.objects.create(title="Very High Priority", priority=100)
        logger.info(f"Created task with priority: {task.priority}")
        self.assertEqual(task.priority, 100)  # High priority should save correctly

    # Test to verify that all fields of the task can be set and saved
    def test_task_with_all_fields(self):
        logger.info("Running test_task_with_all_fields to verify all fields")
        
        # Creating a task with all fields populated
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
        
        # Verifying that all the fields have been saved correctly
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "This is a test")
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertEqual(task.due_date, now)
        self.assertEqual(task.priority, 5)

    # Test to verify that the title field cannot be null
    def test_title_not_null(self):
        logger.info("Running test_title_not_null to verify title not null")
        
        # Trying to create a task with a null title
        task = Task(title=None)
        logger.error("Attempted to create task with null title")
        
        # Expecting a ValidationError when trying to save
        with self.assertRaises(ValidationError):
            task.full_clean()
