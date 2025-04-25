from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from datetime import datetime
from django.db.models.functions import TruncDate
from tasks.models import Task

class TaskQueryService:
    def __init__(self, queryset, request):
        self.queryset = queryset
        self.request = request

    def filter_by_search_date(self):
        search_date = self.request.query_params.get('search_date', None)
        if search_date:
            try:
                search_date_obj = datetime.strptime(search_date, "%Y-%m-%d")
                self.queryset = self.queryset.annotate(created_date=TruncDate('created_at')).filter(created_date=search_date_obj.date())
            except ValueError:
                self.queryset = Task.objects.none()
        return self.queryset

    def filter_by_search_title(self):
        search_title = self.request.query_params.get('search', None)
        if search_title:
            self.queryset = self.queryset.annotate(
                similarity=TrigramSimilarity('title', search_title)
            ).filter(similarity__gt=0.1).order_by('-similarity')
        return self.queryset

    def sort_by_date(self):
        sort_by_date = self.request.query_params.get('sort_by_date', None)
        if sort_by_date:
            if sort_by_date == 'true':
                self.queryset = self.queryset.order_by('-created_at')
            elif sort_by_date == 'false':
                self.queryset = self.queryset.order_by('created_at')
        return self.queryset

    def apply_filters(self):
        self.queryset = self.filter_by_search_date()
        self.queryset = self.filter_by_search_title()
        self.queryset = self.sort_by_date()
        return self.queryset