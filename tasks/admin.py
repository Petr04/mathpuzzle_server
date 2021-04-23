from django.contrib import admin

from .models import Task, Question, Answer, Attempt


# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1

class AttemptInline(admin.TabularInline):
    model = Attempt
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline, AttemptInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Task)
admin.site.register(Attempt)
