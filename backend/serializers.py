from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=64)
    check_on_submit = serializers.BooleanField(default=False)
    questions = serializers.StringRelatedField(many=True)

