from django.db import models
from enum import Enum, StrEnum

class TaskStatus(StrEnum):
    """
    Enum class for defining the possible statuses of a task.
    Inherits from StrEnum for ensuring that the values are strings.
    """
    PENDING = 'Pending'
    COMPLETED = 'Completed'

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples for use in Django's `choices` field option.
        Each tuple contains a key and the corresponding string value.
        """
        return [(key, key.value) for key in cls]

class BaseModel(models.Model):
    """
    Abstract base model that provides common fields (ID, creation, and update timestamps)
    for other models to inherit from.
    """

    id = models.AutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated At")

    class Meta:
        """
        Meta class defines model-level options.

        - `abstract = True` indicates that this is an abstract model and cannot be used 
          directly for table creation, but can be inherited by other models.
        - `verbose_name` defines the singular name for the model.
        """
        abstract = True
        verbose_name = "Base Fields"

class Task(BaseModel):
    """
    Model representing a Task.
    Inherits from `BaseModel` to include common fields such as ID, creation, and 
    update timestamps.
    """

    title = models.CharField(max_length=255, verbose_name="Task Title", null=False)
    """
    `title`: CharField to store the title of the task.
    - `max_length=255`: Maximum length of the task title.
    - `verbose_name="Task Title"`: A human-readable name for the field.
    - `null=False`: Ensures that the field cannot be null.
    """

    description = models.TextField(blank=True, verbose_name="Task Description")
    """
    `description`: TextField to store the description of the task.
    - `blank=True`: Allows this field to be left blank.
    - `verbose_name="Task Description"`: A human-readable name for the field.
    """

    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices(),
        default=TaskStatus.PENDING,
        verbose_name="Task Status"
    )
    """
    `status`: CharField to store the status of the task (Pending or Completed).
    - `max_length=20`: Defines the maximum length for the status field.
    - `choices=TaskStatus.choices()`: Uses the TaskStatus enum class for allowed values.
    - `default=TaskStatus.PENDING`: Sets the default value to 'Pending' when not provided.
    - `verbose_name="Task Status"`: A human-readable name for the field.
    """

    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Due Date")
    """
    `due_date`: DateTimeField to store the task's due date and time.
    - `null=True`: Allows the due date to be null.
    - `blank=True`: Allows the field to be left blank.
    - `verbose_name="Due Date"`: A human-readable name for the field.
    """

    priority = models.IntegerField(default=0, verbose_name="Priority Level")
    """
    `priority`: IntegerField to store the task's priority level.
    - `default=0`: Sets the default priority level to 0 if not provided.
    - `verbose_name="Priority Level"`: A human-readable name for the field.
    """

    class Meta:
        """
        Meta class to define model-level options.
        - `verbose_name`: The singular name of the model for the admin interface.
        - `verbose_name_plural`: The plural name of the model for the admin interface.
        - `ordering`: Defines the default ordering for the records when queried from the database.
        """
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-created_at']  # Orders tasks by the most recent ones first.

    def __str__(self):
        """
        String representation of the Task object.
        Returns a string in the format "Task Title (Status)".
        """
        return f"{self.title} ({self.status})"