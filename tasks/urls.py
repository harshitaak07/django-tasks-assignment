from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# Create an instance of DefaultRouter, which will automatically generate the URL patterns for the ViewSet
router = DefaultRouter()
# Register the TaskViewSet with the router. 
# The 'r' in the URL path indicates that the route is for the Task model, and 'task' is the basename used for reverse URL lookups.
router.register(r'', TaskViewSet, basename='task')

# Define the URL patterns to include the generated routes from the router
urlpatterns = [
    path('', include(router.urls)),
]