import logging
from rest_framework.exceptions import ValidationError
from tasks.models import Task, TaskStatus
from tasks.serializer import TaskSerializer
from django.test import TestCase

logger = logging.getLogger('django')

# Test suite for TaskSerializer.
class TaskSerializerTest(TestCase):
    # Test case to verify that valid task data serializes correctly.
    def test_valid_serialization(self):
        logger.info("Running test_valid_serialization to verify valid serialization")
        task_data = {
            "title": "Serialize Test",
            "description": "Testing serializer",
            "status": TaskStatus.COMPLETED,
            "priority": 3,
            "due_date": "2025-04-25T12:00:00Z"
        }
        serializer = TaskSerializer(data=task_data)
        is_valid = serializer.is_valid()
        logger.info(f"Serializer valid: {is_valid}, data: {task_data}")
        self.assertTrue(is_valid)

    # Test case to verify handling of missing required fields.
    def test_missing_title(self):
        logger.info("Running test_missing_title to verify missing title")
        task_data = {
            "description": "Missing title",
            "status": TaskStatus.PENDING,
        }
        serializer = TaskSerializer(data=task_data)
        is_valid = serializer.is_valid()
        logger.warning(f"Serializer valid: {is_valid}, errors: {serializer.errors}")
        self.assertFalse(is_valid)
        self.assertIn("title", serializer.errors)

    # Test case to ensure optional fields like 'description' can be omitted without error.
    def test_missing_optional_description(self):
        logger.info("Running test_missing_optional_description to verify missing optional description")
        task_data = {
            "title": "Missing Description",
            "status": TaskStatus.PENDING,
            "priority": 3,
        }
        serializer = TaskSerializer(data=task_data)
        is_valid = serializer.is_valid()
        logger.info(f"Serializer valid: {is_valid}, data: {task_data}")
        self.assertTrue(is_valid)

    # Test case to ensure invalid values for the 'status' field are caught.
    def test_invalid_status(self):
        logger.info("Running test_invalid_status to verify invalid status")
        task_data = {
            "title": "Invalid Status",
            "status": "UNKNOWN"
        }
        serializer = TaskSerializer(data=task_data)
        is_valid = serializer.is_valid()
        logger.warning(f"Serializer valid: {is_valid}, errors: {serializer.errors}")
        self.assertFalse(is_valid)
        self.assertIn("status", serializer.errors)

    # Test case to ensure that a valid due date string is accepted and serialized correctly.
    def test_valid_due_date(self):
        logger.info("Running test_valid_due_date to verify valid due date")
        valid_due_date = "2025-04-25T12:00:00Z"
        task_data = {
            "title": "Test Task with Due Date",
            "description": "Testing due date serialization",
            "status": TaskStatus.PENDING,
            "due_date": valid_due_date,
            "priority": 3
        }
        serializer = TaskSerializer(data=task_data)
        is_valid = serializer.is_valid()
        logger.info(f"Serializer valid: {is_valid}, data: {task_data}")
        self.assertTrue(is_valid)


    # Test case to verify that missing optional fields like 'due_date' do not cause errors.
    def test_missing_due_date(self):
        logger.info("Running test_missing_due_date to verify missing due date")
        task_data = {
            "title": "Task without Due Date",
            "description": "No due date provided",
            "status": TaskStatus.PENDING,
            "priority": 3
        }
        serializer = TaskSerializer(data=task_data)
        is_valid = serializer.is_valid()
        logger.info(f"Serializer valid: {is_valid}, data: {task_data}")
        self.assertTrue(is_valid)

    # Test case to ensure that an invalid date string (non-ISO format) results in an error.
    def test_invalid_due_date(self):
        logger.info("Running test_invalid_due_date to verify invalid due date")
        task_data = {
            "title": "Invalid Date Task",
            "description": "This should raise an error",
            "status": TaskStatus.PENDING,
            "due_date": "invalid-date-string",
            "priority": 3
        }
        serializer = TaskSerializer(data=task_data)
        is_valid = serializer.is_valid()
        logger.warning(f"Serializer valid: {is_valid}, errors: {serializer.errors}")
        self.assertFalse(is_valid)
        self.assertIn("due_date", serializer.errors)