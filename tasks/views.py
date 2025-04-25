from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializer import TaskSerializer
from tasks.helpers.pagination import TaskPagination
from tasks.helpers.service import TaskQueryService
from tasks.helpers.logger import TaskLogger
from tasks.helpers.filter import TaskFilter

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = TaskPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        TaskLogger.log_task_deletion(instance)
        instance.delete()
        return Response(status=204)

    def get_queryset(self):
        queryset = super().get_queryset()
        query_service = TaskQueryService(queryset, self.request)
        return query_service.apply_filters()

    def partial_update(self, request, *args, **kwargs):
        task_instance = self.get_object()
        TaskLogger.log_task_update(task_instance)
        return super().partial_update(request, *args, **kwargs)