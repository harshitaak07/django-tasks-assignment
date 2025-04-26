from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from datetime import datetime
from django.db.models.functions import TruncDate
from tasks.models import Task

class TaskQueryService:
    # A service class to handle filtering and sorting of task querysets.
    def __init__(self, queryset, request):
        # Initializes the TaskQueryService with a queryset and the request object.
        self.queryset = queryset
        self.request = request

    def filter_by_search_date(self):
        # Filters the queryset by a specific creation date if provided in the request.
        search_date = self.request.query_params.get('search_date', None)
        if search_date:
            try:
                search_date_obj = datetime.strptime(search_date, "%Y-%m-%d")
                self.queryset = self.queryset.annotate(created_date=TruncDate('created_at')).filter(created_date=search_date_obj.date())
            except ValueError:
                # If the date format is invalid, return an empty queryset.
                self.queryset = Task.objects.none()
        return self.queryset

    def filter_by_search_title(self):
        # Filters the queryset by a search term in the task title using trigram similarity.
        search_title = self.request.query_params.get('search', None)
        if search_title:
            self.queryset = self.queryset.annotate(
                similarity=TrigramSimilarity('title', search_title)
            ).filter(similarity__gt=0.1).order_by('-similarity')
        return self.queryset

    def sort_by_date(self):
        # Sorts the queryset by the creation date based on the `sort_by_date` query parameter.
        sort_by_date = self.request.query_params.get('sort_by_date', None)
        if sort_by_date:
            if sort_by_date == 'true':
                self.queryset = self.queryset.order_by('-created_at')
            elif sort_by_date == 'false':
                self.queryset = self.queryset.order_by('created_at')
        return self.queryset

    def apply_filters(self):
        # Applies all filters (search date, search title, and sorting by date) to the queryset.
        self.queryset = self.filter_by_search_date()
        self.queryset = self.filter_by_search_title()
        self.queryset = self.sort_by_date()
        return self.queryset
