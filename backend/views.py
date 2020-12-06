from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer, QuestionSerializer


# Create your views here.

class TasksView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        tasks_serializer = TaskSerializer(tasks, many=True)

        return Response({"tasks": tasks_serializer.data})

    def post(self, request):
        task = request.data.get('task')
        task_serializer = TaskSerializer(data=task)
        if task_serializer.is_valid(raise_exception=True):
            task_saved = task_serializer.save()
        return Response({'success': "Task '{}' created successfully".format(task_saved.title)})


class QuestionsView(APIView):
    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        question_serializer = QuestionSerializer(task.questions, many=True)
        return Response({"questions": question_serializer.data})

    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        data = request.data
        question = list(task.questions.all())[data["question_num"]]
        if data['type'] == 'text_field':
            answer = question.answers.get(answer_num=0)
            return Response({'correct': data['answer'] == answer.text})
        elif data['type'] == 'choice_field':
            answer = question.answers.get(answer_num=int(data['answer']))
            return Response({"correct": answer.is_true})
