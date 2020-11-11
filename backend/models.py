from django.db import models


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=64, null=True)
    check_on_submit = models.BooleanField()

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="questions")
    attempts = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class TextQuestion(Question):
    text = models.TextField()
    answer = models.CharField(max_length=32)
    type = 'textQuestion'
