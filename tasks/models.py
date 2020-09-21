from django.db import models

import json


class Question(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)

    def __str__(self):
        return self.title or f'{self.type} id={self.id}'

    class Meta:
        abstract = True

class TextQuestion(Question):
    text = models.TextField()
    answer = models.CharField(max_length=32)
    type = 'textQuestion'

class ChoiceQuestion(Question):
    text = models.TextField()
    choices = models.TextField()

    # When used PostgreSQL choices shold be JSONField

    def set_choices(self, x):
        self.choices = json.dumps(x)

    def get_choices(self):
        return json.loads(self.choices)

    answer = models.IntegerField()

    type = 'choiceQuestion'


class Task(models.Model):
    title = models.CharField(max_length=64, null=True)

    # check only when entire task is submitted
    check_on_submit = models.BooleanField()

    @property
    def questions(self):
        ret = []
        for Sub in Question.__subclasses__():
            ret += Sub.objects.filter(task=self)

        return ret

    def __str__(self):
        return self.title
