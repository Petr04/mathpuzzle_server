from django.contrib import admin

from .models import Task, Question, Answer


# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Task)
