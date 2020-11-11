import json

from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)  # 0 as infinity

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
        return json.loads(self.choices.encode('unicode_escape'))

    answer = models.IntegerField()

    type = 'choiceQuestion'


type_to_model = {}
for Q in Question.__subclasses__():
    type_to_model[Q.type] = Q


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
