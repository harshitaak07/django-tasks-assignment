import django_filters
from tasks.models import Task

class TaskFilter(django_filters.FilterSet):
    """
    A filter class for filtering Task objects based on specific criteria.

    Filters:
    - search_date: Filters tasks created on a specific date.
    - search: Filters tasks by title (case-insensitive partial match).
    - sort_by_date: Sorts tasks by creation date (ascending or descending).
    """
    search_date = django_filters.DateFilter(field_name="created_at", lookup_expr='date', label="Created Date")
    search = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label="Title")
    sort_by_date = django_filters.BooleanFilter(method='filter_sort_by_date', label="Sort by Date")

    class Meta:
        model = Task
        fields = ['search_date', 'search', 'sort_by_date']

    def filter_sort_by_date(self, queryset, name, value):
        """
        Custom filter to sort tasks by their creation date.
        If value is True, it will sort in descending order, otherwise ascending.

        Args:
        queryset (QuerySet): The queryset to be filtered.
        name (str): The name of the filter.
        value (bool): Whether to sort in descending (True) or ascending (False) order.

        Returns:
        QuerySet: The sorted queryset.
        """
        if value:
            return queryset.order_by('-created_at')
        return queryset.order_by('created_at')
