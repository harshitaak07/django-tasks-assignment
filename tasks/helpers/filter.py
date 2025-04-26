import django_filters
from tasks.models import Task

class TaskFilter(django_filters.FilterSet):
    # A filter class for filtering Task objects based on specific criteria.
    search_date = django_filters.DateFilter(field_name="created_at", lookup_expr='date', label="Created Date")
    search = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label="Title")
    sort_by_date = django_filters.BooleanFilter(method='filter_sort_by_date', label="Sort by Date")

    class Meta:
        model = Task
        fields = ['search_date', 'search', 'sort_by_date']

    def filter_sort_by_date(self, queryset, name, value):
        # Custom filter to sort tasks by their creation date.
        if value:
            return queryset.order_by('-created_at')
        return queryset.order_by('created_at')
