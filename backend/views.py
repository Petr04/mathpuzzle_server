from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task
from .serializers import TaskSerializer, TextQuestionSerializer, ChoiceQuestionSerializer


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
        text_question_serializer = TextQuestionSerializer(task.text_questions, many=True)
        choice_question_serializer = ChoiceQuestionSerializer(task.choice_questions, many=True)
        return Response({"text_questions": text_question_serializer.data,
                         "choice_questions": choice_question_serializer.data})

    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        data = request.data
        if data['type'] == 'text_field':
            question = task.text_questions.get(question_num=data['question_num'])
            return Response({'correct': data['answer'] == question.answer})
        elif data['type'] == 'choice_field':
            question = task.choice_questions.get(question_num=data['question_num'])
            answer = question.answers.get(answer_num=int(data['answer']))
            return Response({"correct": answer.is_true})
