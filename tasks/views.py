from django.http import HttpResponseForbidden

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from .models import Task, Question, Attempt, \
    TextChoiceAttemptAnswer, OrderAttemptAnswer
from userapi.models import User
from .serializers import TaskSerializer, QuestionSerializer, \
    ChoiceQuestionSerializer, OrderQuestionSerializer, AttemptSerializer

import json


# Create your views here.

class TasksView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        tasks = Task.objects.all().order_by('-id')

        if request.GET.get('filter'):
            tasks = tasks.filter(title__contains=request.GET['filter'])

        if 'limit' in request.GET:
            limit = int(request.GET['limit'])
            offset = int(request.GET.get('offset') or 0)
            tasks = tasks[offset:offset+limit]

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

        # Checking correctness
        if question.type == 'textQuestion':
            correct = question.answers.get(
                answer_num=0).text == request.GET['answer']
        elif question.type == 'choiceQuestion':
            correct = question.answers.get(
                answer_num=int(request.GET['answer'])).is_true
        elif question.type == 'orderQuestion':
            answers = list(map(lambda x: x.text, question.answers.all()))
            request_answers = dict(request.GET)['answers']
            correct = answers == request_answers

        # Saving attempt
        if not request.user.is_anonymous:

            attempt = Attempt.objects.create(
                question=question,
                user=request.user,
                value=correct,
            )

            if question.type in ['textQuestion', 'choiceQuestion']:
                answer = TextChoiceAttemptAnswer.objects.create(
                    attempt=attempt,
                    value=request.GET['answer']
                )
            elif question.type == 'orderQuestion':
                answer = OrderAttemptAnswer.objects.create(
                    attempt=attempt,
                    value=json.dumps(request_answers)
                )

            attempt.answer = answer

            attempt.save()

        return Response({'correct': correct})


def exclude_keys(d, keys):
    return {k: v for k, v in d.items() if k not in keys}

class AttemptsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        filters = {}

        if 'task' in request.GET:
            filters['question__task'] = request.GET['task']

        filters.update(
            exclude_keys(dict(request.GET.items()), ('task', 'last'))
        )

        semi_filtered = Attempt.objects.filter(**filters)
        filtered_object_list = []
        for attempt in semi_filtered:
            if request.user in (attempt.user, attempt.question.task.author):
                filtered_object_list.append(attempt)

        ret = Attempt.objects.filter(id__in=map(lambda x: x.id, filtered_object_list))

        if request.GET.get('last'):
            # get last attempt from each user per question

            if 'question' in request.GET:
                questions = Question.objects.filter(
                    id=request.GET['question'])
            elif 'task' in request.GET:
                questions = Question.objects.filter(
                    task=request.GET['task'])

            last_attempt_list = Attempt.last(questions)

            return Response( AttemptSerializer(last_attempt_list, many=True).data )

        return Response( AttemptSerializer(ret, many=True).data )
