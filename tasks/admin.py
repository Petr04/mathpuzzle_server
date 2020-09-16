from django.contrib import admin

from . import models

admin.site.register(models.TextQuestion)
admin.site.register(models.Task)
