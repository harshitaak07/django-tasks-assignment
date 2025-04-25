import django_filters
from tasks.models import Task

class TaskFilter(django_filters.FilterSet):
    search_date = django_filters.DateFilter(field_name="created_at", lookup_expr='date')
    search = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    sort_by_date = django_filters.BooleanFilter(method='filter_sort_by_date')

    class Meta:
        model = Task
        fields = ['search_date', 'search', 'sort_by_date']

    def filter_sort_by_date(self, queryset, name, value):
        if value:
            return queryset.order_by('-created_at')
        return queryset.order_by('created_at')
