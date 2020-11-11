from django.urls import path

from . import views

app_name = 'backend'

urlpatterns = [
    path('tasks', views.AllTasksView.as_view())
]
