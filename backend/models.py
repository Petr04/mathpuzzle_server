from django.db import models


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=64, null=True)
    check_on_submit = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)
    text = models.TextField()
    attempts = models.IntegerField(default=0)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='questions')
    type_choices = (('text_question', 'text_question'), ('choice_question', 'choice_question'))
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
