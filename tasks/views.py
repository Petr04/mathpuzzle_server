from django.http import JsonResponse

from time import sleep
from functools import reduce

from .models import Task, Question, TextQuestion


def all(request):
    response = {}
    for task in Task.objects.all():
        question_titles = [question.title for question in task.questions]

        response[task.id] = {
            'id': task.id,
            'title': task.title,
            'text': '\n'.join(question_titles),
        }

    # for loading animation demo
    # sleep(2)

    return JsonResponse(response)

def detail(request, id):
    task = Task.objects.get(id=id)
    response = {
        'title': task.title,
        'checkOnSubmit': task.check_on_submit,
        'questions': [],
    }
    for question in task.questions:
        question_resp = {
            'type': question.type,
        }
        if question.type == 'text_question':
            question_resp.update({
                'id': question.id,
                'type': question.type,
                'title': question.title,
                'text': question.text,
            })
        response['questions'].append(question_resp)

    # sleep(2)

    return JsonResponse(response)

def check(request, id):
    # можно будет потом вынести в переменную / функцию
    questions = reduce(lambda x, y: x + y, [Sub.objects.all() for Sub in Question.__subclasses__()])
    question = questions.get(id=id)
    correct = request.GET['answer'] == question.answer

    # sleep(2)

    return JsonResponse({'correct': correct})
