from django.http import JsonResponse, Http404

from time import sleep
from itertools import chain

from .models import Task, Question, TextQuestion


def all(request):
    response = {}
    for task in Task.objects.all():
        question_titles = filter(lambda x: type(x) == str and x.strip(),
            [question.title for question in task.questions])

        response[task.id] = {
            'id': task.id,
            'title': task.title,
            'length': len(task.questions),
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
        question_resp = { # Common props
            'id': question.id,
            'type': question.type,
            'title': question.title,
            'text': question.text,
        }

        # Type-special props

        if question.type == 'choiceQuestion':
            question_resp.update({
                'choices': question.get_choices(),
            })

        response['questions'].append(question_resp)

    # sleep(2)

    return JsonResponse(response)

def check(request, id):
    # Можно будет потом вынести в переменную / функцию
    questions = chain([Sub.objects.all() for Sub in Question.__subclasses__()])
    exists = False
    for query_set in questions:
        try: question = query_set.get(id=id)
        except: pass
        else: exists = True

    if not exists: return Http404()

    if question.type == 'choiceQuestion':
        request_answer = int(request.GET['answer'])
    else: request_answer = request.GET['answer']

    correct = request_answer == question.answer

    # sleep(2)

    return JsonResponse({'correct': correct})
