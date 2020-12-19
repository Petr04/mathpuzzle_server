from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, Question
from .serializers import TaskSerializer, GetTaskSerializer, \
    TaskSerializerNoQuestions, QuestionSerializer, ChoiceQuestionSerializer


# Create your views here.

class TasksView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        tasks_serializer = GetTaskSerializer(tasks, many=True)

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
        task_serializer = TaskSerializerNoQuestions(task)

        print(task.questions.filter(type="choiceQuestion"))
        question_serializer = QuestionSerializer(
            task.questions.exclude(type="choiceQuestion"), many=True)
        choice_question_serializer = ChoiceQuestionSerializer(
            task.questions.filter(type="choiceQuestion"), many=True)

        return Response({
            "data": task_serializer.data,
            "questions": question_serializer.data
                + choice_question_serializer.data,
        })


class CheckView(APIView):
    def get(self, request, pk):
        question = Question.objects.get(id=pk)

        if question.type == 'textQuestion':
            correct = question.answers.get(answer_num=0).text == request.GET['answer']
        elif question.type == 'choiceQuestion':
            correct = question.answers.get(answer_num=int(request.GET['answer'])).is_true

        return Response({'correct': correct})
