from rest_framework import serializers
from .models import Task, TaskStatus

class TaskSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=TaskStatus.choices(), default=TaskStatus.PENDING)
    class Meta:
        model = Task
        fields = '__all__'