from django.urls import path

from . import views

app_name = 'backend'

urlpatterns = [
    path('', views.TasksView.as_view()),
    path('<int:pk>/', views.QuestionsView.as_view()),
    path('check/<int:pk>/', views.CheckView.as_view()),
]
