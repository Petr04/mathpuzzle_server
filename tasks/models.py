from django.db import models
from userapi.models import User


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=64)
    check_on_submit = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title

    def is_finished(self, user):
        finished = True
        for question in Question.objects.filter(task=self):
            finished &= question.is_finished(user)

        return finished

    def get_status(self, user):
        if self.is_finished(user):
            return 'finished'

        questions = Question.objects.filter(task=self)
        attempts = Attempt.objects.filter(question__in=questions, user=user)

        if len(attempts) > 0:
            return 'started'

        return 'default'


class Question(models.Model):
    title = models.CharField(max_length=32)
    text = models.TextField()
    attempts_max = models.IntegerField(default=0)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='questions')
    type_choices = [(choice, choice) for choice in (
        'textQuestion', 'choiceQuestion', 'orderQuestion'
    )]
    type = models.CharField(choices=type_choices,
                            max_length=16)

    def __str__(self):
        return self.title

    def attempts_number(self):
        return Attempt.objects.filter(question=self).count()

    def is_finished(self, user):
        attempts = Attempt.objects.filter(question=self, user=user)
        return attempts.filter(value=True).count() > 0 \
            or (attempts.count() >= self.attempts_max
                and self.attempts_max > 0)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer_num = models.IntegerField()
    text = models.CharField(max_length=64)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Attempt(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    answer = models.CharField(max_length=64)
    value = models.BooleanField()

    def last(questions):
        lastUserAttemptIDs = []
        for question in list(questions):
            emailSet = list(map(lambda x: x[0],
                set(question.attempts.values_list('user'))))

            for email in emailSet:
                user = User.objects.get(email=email)
                id_ = (
                    Attempt.objects.filter(user=user)
                    & Attempt.objects.filter(question=question)
                ).last().id
                lastUserAttemptIDs.append(id_)

        return Attempt.objects.filter(id__in=lastUserAttemptIDs)
