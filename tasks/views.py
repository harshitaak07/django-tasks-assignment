from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django_ratelimit.core import is_ratelimited

from .models import Task
from .serializer import TaskSerializer
from tasks.helpers.pagination import TaskPagination
from tasks.helpers.service import TaskQueryService
from tasks.helpers.logger import TaskLogger
from tasks.helpers.filter import TaskFilter

 # Default queryset for fetching tasks
 
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer  # Serializer class for serializing task objects
    pagination_class = TaskPagination  # Custom pagination class to control how many tasks per page
    filter_backends = (DjangoFilterBackend,)  # Django filter backend to apply custom filtering to tasks
    filterset_class = TaskFilter  # Custom filter class for filtering tasks based on various fields

    # Custom delete action, overriding the default destroy behavior
    def destroy(self, request, *args, **kwargs): 
        if is_ratelimited(request, group='delete-task',key='user', rate='2/m', method='DELETE', increment=True):
            return Response({'detail': 'Rate limit exceeded. Try again later.'}, status=429)
        instance = self.get_object()  # Retrieve the task object that is to be deleted
        TaskLogger.log_task_deletion(instance)  
        instance.delete()  # Delete the task from the database
        return Response(status=204)  
    
    # Custom queryset method to apply filters based on the request
    def get_queryset(self):  
        queryset = super().get_queryset()  
        query_service = TaskQueryService(queryset, self.request)  # Use the TaskQueryService to apply any filters from the request  
        return query_service.apply_filters() 
    
    # Custom partial update method, overriding the default behavior
    def partial_update(self, request, *args, **kwargs):
        if is_ratelimited(request, group='update-task',key='user', rate='2/m', method='PATCH', increment=True):
            return Response({'detail': 'Rate limit exceeded. Try again later.'}, status=429)
        task_instance = self.get_object()  # Get the task object that needs to be updated
        TaskLogger.log_task_update(task_instance)
        return super().partial_update(request, *args, **kwargs)