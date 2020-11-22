from django.urls import path

from . import views

app_name = 'backend'

urlpatterns = [
    path('tasks', views.TasksView.as_view()),
    path('tasks/<int:pk>', views.QuestionsView.as_view())
]
