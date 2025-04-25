from rest_framework.exceptions import ValidationError
from tasks.models import Task, TaskStatus
from tasks.serializer import TaskSerializer
from django.test import TestCase
from datetime import datetime

class TaskSerializerTest(TestCase):
    def test_valid_serialization(self):
        task_data = {
            "title": "Serialize Test",
            "description": "Testing serializer",
            "status": TaskStatus.COMPLETED,
            "priority": 3,
            "due_date": "2025-04-25T12:00:00Z"  
        }
        serializer = TaskSerializer(data=task_data)
        self.assertTrue(serializer.is_valid())

    def test_missing_title(self):
        task_data = {
            "description": "Missing title",
            "status": TaskStatus.PENDING,
        }
        serializer = TaskSerializer(data=task_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
    
    def test_missing_optional_description(self):
        task_data = {
            "title": "Missing Description",
            "status": TaskStatus.PENDING,
            "priority": 3,
        }
        serializer = TaskSerializer(data=task_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_status(self):
        task_data = {
            "title": "Invalid Status",
            "status": "UNKNOWN"
        }
        serializer = TaskSerializer(data=task_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)

    def test_valid_due_date(self):
        valid_due_date = "2025-04-25T12:00:00Z" 
        task_data = {
            "title": "Test Task with Due Date",
            "description": "Testing due date serialization",
            "status": TaskStatus.PENDING,
            "due_date": valid_due_date,
            "priority": 3
        }
        serializer = TaskSerializer(data=task_data)
        self.assertTrue(serializer.is_valid())

    def test_missing_due_date(self):
        task_data = {
            "title": "Task without Due Date",
            "description": "No due date provided",
            "status": TaskStatus.PENDING,
            "priority": 3
        }
        serializer = TaskSerializer(data=task_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_due_date(self):
        task_data = {
            "title": "Invalid Date Task",
            "description": "This should raise an error",
            "status": TaskStatus.PENDING,
            "due_date": "invalid-date-string", 
            "priority": 3
        }
        serializer = TaskSerializer(data=task_data)
        self.assertFalse(serializer.is_valid())  
        self.assertIn("due_date", serializer.errors)