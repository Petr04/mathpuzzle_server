from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer


# Create your views here.

class AllTasksView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        tasks_serializer = TaskSerializer(tasks, many=True)
        return Response({"tasks": tasks_serializer.data})
