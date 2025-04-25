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
    # Default queryset for fetching tasks
    queryset = Task.objects.all()
    
    # Serializer class for serializing task objects
    serializer_class = TaskSerializer
    
    # Custom pagination class to control how many tasks per page
    pagination_class = TaskPagination
    
    # Django filter backend to apply custom filtering to tasks
    filter_backends = (DjangoFilterBackend,)
    
    # Custom filter class for filtering tasks based on various fields
    filterset_class = TaskFilter

    # Custom delete action, overriding the default destroy behavior
    def destroy(self, request, *args, **kwargs):
        # Retrieve the task object that is to be deleted
        instance = self.get_object()
        
        # Log the deletion of the task using a custom logger
        TaskLogger.log_task_deletion(instance)
        
        # Delete the task from the database
        instance.delete()
        
        # Return a 204 No Content status to indicate successful deletion
        return Response(status=204)

    # Custom queryset method to apply filters based on the request
    def get_queryset(self):
        # Get the default queryset
        queryset = super().get_queryset()
        
        # Use the TaskQueryService to apply any filters from the request
        query_service = TaskQueryService(queryset, self.request)
        
        # Return the filtered queryset
        return query_service.apply_filters()

    # Custom partial update method, overriding the default behavior
    def partial_update(self, request, *args, **kwargs):
        # Get the task object that needs to be updated
        task_instance = self.get_object()
        
        # Log the update of the task using a custom logger
        TaskLogger.log_task_update(task_instance)
        
        # Call the default partial update method to apply changes
        return super().partial_update(request, *args, **kwargs)