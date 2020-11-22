from django.db import models


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=64, null=True)
    check_on_submit = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)
    question_num = models.IntegerField()
    text = models.TextField()
    attempts = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class TextQuestion(Question):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='text_questions')
    answer = models.CharField(max_length=32)
    type = 'text_field'


class ChoiceQuestion(Question):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='choice_questions')
    type = 'choice_field'


class Answer(models.Model):
    question = models.ForeignKey(ChoiceQuestion, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=64)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.text
