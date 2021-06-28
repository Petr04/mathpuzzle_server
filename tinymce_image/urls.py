from django.urls import path

from . import views

app_name = 'tinymce_image'

urlpatterns = [
    path('upload/', views.upload),
    path('download/<path:path>/', views.download),
]
