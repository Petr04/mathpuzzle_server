from django.http import HttpResponseForbidden

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from .models import Task, Question, Attempt
from userapi.models import User
from .serializers import TaskSerializer, QuestionSerializer, \
    ChoiceQuestionSerializer, OrderQuestionSerializer, AttemptSerializer


# Create your views here.

class TasksView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        tasks = Task.objects.all().order_by('-id')
        tasks_serializer = TaskSerializer(tasks, many=True, context={
            'short': True,
            'request': request,
        })

        return Response({"tasks": tasks_serializer.data})

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        task = request.data.get('task')
        task_serializer = TaskSerializer(data=task, context={
            'request': request
        })
        if task_serializer.is_valid(raise_exception=True):
            task_saved = task_serializer.save()
        return Response({'success': "Task '{}' created successfully"
            .format(task_saved.title)})


class QuestionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        task_serializer = TaskSerializer(task, context={
            'request': request
        })

        question_serializer = QuestionSerializer(
            task.questions.filter(type="textQuestion"), many=True)
        choice_question_serializer = ChoiceQuestionSerializer(
            task.questions.filter(type="choiceQuestion"), many=True)
        order_question_serializer = OrderQuestionSerializer(
            task.questions.filter(type="orderQuestion"), many=True)

        question_data = sorted(
            question_serializer.data
            + choice_question_serializer.data
            + order_question_serializer.data,
            key=lambda question: question['id']
        )

        return Response({
            **task_serializer.data,
            "questions": question_data,
        })


class CheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        question = Question.objects.get(id=pk)

        if question.type == 'textQuestion':
            correct = question.answers.get(
                answer_num=0).text == request.GET['answer']
        elif question.type == 'choiceQuestion':
            correct = question.answers.get(
                answer_num=int(request.GET['answer'])).is_true

        attempt = Attempt.objects.create(
            question=question,
            user=request.user,
            value=correct,
            answer=request.GET['answer']
        )
        attempt.save()

        return Response({'correct': correct})


def exclude_keys(d, keys):
    return {k: v for k, v in d.items() if k not in keys}

class AttemptsView(ListAPIView):
    serializer_class = AttemptSerializer
    def get_queryset(self):
        filters = {}

        if 'task' in self.request.GET:
            filters['question__task'] = self.request.GET['task']
        filters.update(
            exclude_keys(dict(self.request.GET.items()), ('task', 'last'))
        )

        ret = Attempt.objects.filter(**filters)

        if self.request.GET.get('last'):
            # get last attempt from each user per question

            if 'question' in self.request.GET:
                questions = Question.objects.filter(
                    id=self.request.GET['question'])
            elif 'task' in self.request.GET:
                questions = Question.objects.filter(
                    task=self.request.GET['task'])

            return Attempt.last(questions)

        return ret
