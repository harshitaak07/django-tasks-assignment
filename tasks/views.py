from rest_framework import viewsets
from .serializer import TaskSerialize
from .models import Task


class TaskView(viewsets.ModelViewSet):
    # Create your views here.
    pass