from rest_framework import serializers
from .models import Task, TaskStatus

class TaskSerializer(serializers.ModelSerializer):
    # Serializer for the Task model. It converts Task instances to JSON format and
    
    status = serializers.ChoiceField(choices=TaskStatus.choices(), default=TaskStatus.PENDING)
    # `status`: A field that validates the status of the task.
    class Meta:
        # The `Meta` class is used to configure the serializer's behavior.
        model = Task
        fields = '__all__' # Include all fields in the serializer.