from os import truncate
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import TruncDate
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Task
from .serializer import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
    
    def get_queryset(self):
        queryset = Task.objects.all()

        search_date = self.request.query_params.get('search_date', None)
        if search_date:
            try:
                search_date_obj = datetime.strptime(search_date, "%Y-%m-%d")
                queryset = queryset.annotate(created_date=TruncDate('created_at')).filter(created_date=search_date_obj.date())
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)


        search_title = self.request.query_params.get('search', None)
        if search_title:
            queryset = queryset.annotate(
                similarity=TrigramSimilarity('title', search_title)
            ).filter(similarity__gt=0.1).order_by('-similarity')

        sort_by_date = self.request.query_params.get('sort_by_date', None)
        if sort_by_date:
            if sort_by_date == 'true':
                queryset = queryset.order_by('-created_at')
            elif sort_by_date == 'false':
                queryset = queryset.order_by('created_at')

        return queryset

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)