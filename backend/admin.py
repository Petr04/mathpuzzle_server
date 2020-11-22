from django.contrib import admin

from .models import TextQuestion, Task, ChoiceQuestion, Answer


# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1


class ChoiceQuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(TextQuestion)
admin.site.register(ChoiceQuestion, ChoiceQuestionAdmin)
admin.site.register(Task)
