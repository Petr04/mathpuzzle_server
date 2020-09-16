from django.db import models

class Question(models.Model):
    title = models.CharField(max_length=32, null=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)

    class Meta:
        abstract = True

class TextQuestion(Question):
    text = models.TextField()
    answer = models.CharField(max_length=16)
    type = 'text_question'


class Task(models.Model):
    title = models.CharField(max_length=32, null=True)

    @property
    def questions(self):
        ret = []
        for Sub in Question.__subclasses__():
            ret += Sub.objects.filter(task=self)

        return ret
