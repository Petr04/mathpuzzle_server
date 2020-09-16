from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.all),
    path('<int:id>', views.detail),
]
