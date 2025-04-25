from rest_framework.pagination import PageNumberPagination

class TaskPagination(PageNumberPagination):
    """
    Custom pagination class for paginating task lists.

    This class allows for pagination of task data, with configurable page size and the ability
    to modify the page size via query parameters.

    Attributes:
    - page_size: The default number of tasks per page (10).
    - page_size_query_param: The query parameter that can be used to override the page size (`page_size`).
    - max_page_size: The maximum number of tasks that can be returned in a single page (100).
    """
    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100