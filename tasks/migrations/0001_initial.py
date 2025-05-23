# Generated by Django 5.2 on 2025-04-24 20:21

import tasks.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Last Updated At"),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Task Title")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Task Description"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            (tasks.models.TaskStatus["PENDING"], "Pending"),
                            (tasks.models.TaskStatus["COMPLETED"], "Completed"),
                        ],
                        default=tasks.models.TaskStatus["PENDING"],
                        max_length=10,
                        verbose_name="Task Status",
                    ),
                ),
                (
                    "due_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Due Date"
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(default=0, verbose_name="Priority Level"),
                ),
            ],
            options={
                "verbose_name": "Task",
                "verbose_name_plural": "Tasks",
                "ordering": ["-created_at"],
            },
        ),
    ]
