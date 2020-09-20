from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=32, null=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True

class TextQuestion(Question):
    text = models.TextField()
    answer = models.CharField(max_length=16)
    type = 'text_question'


class Task(models.Model):
    title = models.CharField(max_length=32, null=True)

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
