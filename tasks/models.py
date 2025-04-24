from django.db import models
from enum import Enum

class TaskStatus(Enum):
    PENDING = 'Pending'
    COMPLETED = 'Completed'

    @classmethod
    def choices(cls):
        return [(key, key.value) for key in cls]

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated At")

    class Meta:
        abstract = True
        verbose_name = "Base Fields"
class Task(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Task Title")
    description = models.TextField(blank=True, verbose_name="Task Description")
    status = models.CharField(
        max_length=10,
        choices=TaskStatus.choices(),  # Use the choices defined in Enum
        default=TaskStatus.PENDING,
        verbose_name="Task Status"
    )
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Due Date")
    priority = models.IntegerField(default=0, verbose_name="Priority Level")

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-created_at']
        db_table = "task"

    def __str__(self):
        return f"{self.title} ({self.status})"
