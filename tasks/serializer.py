from rest_framework import serializers
from .models import Task, TaskStatus

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model. It converts Task instances to JSON format and 
    validates incoming data when creating or updating tasks.
    """
    
    # `status`: A field that validates the status of the task.
    # It uses `ChoiceField` to ensure the status is one of the predefined values 
    # from the `TaskStatus` enum (either 'Pending' or 'Completed').
    status = serializers.ChoiceField(choices=TaskStatus.choices(), default=TaskStatus.PENDING)
    
    class Meta:
        """
        The `Meta` class is used to configure the serializer's behavior.
        - `model`: The model associated with this serializer (in this case, `Task`).
        - `fields`: A list or tuple of fields that should be included in the serialized output.
          - `'__all__'` includes all fields from the `Task` model.
        """
        model = Task
        fields = '__all__'