from django.http import JsonResponse

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

    return JsonResponse(response)

def detail(request, id):
    task = Task.objects.get(id=id)
    response = {
        'title': task.title,
        'questions': [],
    }
    for question in task.questions:
        question_resp = {
            'type': question.type,
        }
        if question.type == 'text_question':
            question_resp.update({
                'text': question.text,
                'answer': question.answer,
            })
        response['questions'].append(question_resp)

    return JsonResponse(response)
