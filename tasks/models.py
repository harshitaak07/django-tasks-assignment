from django.db import models
from enum import Enum, StrEnum

class TaskStatus(StrEnum):
    # Enum class for defining the possible statuses of a task.
    PENDING = 'Pending'
    COMPLETED = 'Completed'

    @classmethod
    def choices(cls):
        # Returns a list of tuples for use in Django's `choices` field option.
        return [(key, key.value) for key in cls]

class BaseModel(models.Model):
    # Abstract base model that provides common fields (ID, creation, and update timestamps)
    id = models.AutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated At")

    class Meta:
        # Meta class defines model-level options.
        abstract = True
        verbose_name = "Base Fields"

class Task(BaseModel):
    # Model representing a Task.

    title = models.CharField(max_length=255, verbose_name="Task Title", null=False)
    # `title`: CharField to store the title of the task.

    description = models.TextField(blank=True, verbose_name="Task Description")
    # `description`: TextField to store the description of the task.

    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices(),
        default=TaskStatus.PENDING,
        verbose_name="Task Status"
    )
    # `status`: CharField to store the status of the task (Pending or Completed).

    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Due Date")
    # `due_date`: DateTimeField to store the task's due date and time.
    priority = models.IntegerField(default=0, verbose_name="Priority Level")
    # `priority`: IntegerField to store the task's priority level.

    class Meta:
        # Meta class to define model-level options.
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-created_at']  # Orders tasks by the most recent ones first.

    def __str__(self):
        # String representation of the Task object.
        return f"{self.title} ({self.status})"