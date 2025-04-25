import logging
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import TruncDate
from django.db.models import Q
from datetime import datetime
from .models import Task
from .serializer import TaskSerializer
from .pagination import TaskPagination

logger = logging.getLogger('django')

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = TaskPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(f"Deleting Task: {instance.title} (ID: {instance.id})")
        instance.delete()
        return Response(status=204)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_date = self.request.query_params.get('search_date', None)
        
        if search_date:
            try:
                search_date_obj = datetime.strptime(search_date, "%Y-%m-%d")
                queryset = queryset.annotate(created_date=TruncDate('created_at')).filter(created_date=search_date_obj.date())
                logger.info(f"Filtering tasks by search_date: {search_date_obj.date()}")
            except ValueError:
                logger.warning(f"Invalid search_date format: {search_date}")
                queryset = Task.objects.none()

        search_title = self.request.query_params.get('search', None)
        if search_title:
            queryset = queryset.annotate(
                similarity=TrigramSimilarity('title', search_title)
            ).filter(similarity__gt=0.1).order_by('-similarity')
            logger.info(f"Searching tasks by title: {search_title} with similarity filter")

        sort_by_date = self.request.query_params.get('sort_by_date', None)
        if sort_by_date:
            if sort_by_date == 'true':
                queryset = queryset.order_by('-created_at')
                logger.info(f"Sorting tasks by created_at in descending order")
            elif sort_by_date == 'false':
                queryset = queryset.order_by('created_at')
                logger.info(f"Sorting tasks by created_at in ascending order")

        return queryset

    def partial_update(self, request, *args, **kwargs):
        task_instance = self.get_object()
        logger.info(f"Partial update for Task: {task_instance.title} (ID: {task_instance.id})")
        return super().partial_update(request, *args, **kwargs)