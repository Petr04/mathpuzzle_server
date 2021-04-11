from django.db import models
from userapi.models import User


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=64)
    check_on_submit = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=32)
    text = models.TextField()
    attempts_max = models.IntegerField(default=0)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='questions')
    type_choices = (('textQuestion', 'textQuestion'), ('choiceQuestion', 'choiceQuestion'))
    type = models.CharField(choices=type_choices,
                            max_length=16)

    def __str__(self):
        return self.title


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
    value = models.BooleanField()
