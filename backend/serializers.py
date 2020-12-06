from rest_framework import serializers

from .models import Task, Question, Answer


class AnswerSerializer(serializers.Serializer):
    answer_num = serializers.IntegerField()
    text = serializers.CharField()
    is_true = serializers.BooleanField()


class QuestionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=32, allow_blank=True, allow_null=True)
    attempts = serializers.IntegerField()
    text = serializers.CharField()
    type = serializers.ChoiceField(choices=Question.type_choices)
    answers = AnswerSerializer(many=True)

class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    check_on_submit = serializers.BooleanField(default=False)
    questions = QuestionSerializer(many=True, allow_null=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for i in range(len(ret["questions"])):
            ret["questions"][i] = ret["questions"][i]["title"]
        return ret

    def create(self, validated_data):
        questions_data = validated_data.pop("questions")
        task = Task.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop("answers")
            question = Question.objects.create(task=task, **question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)
        return task
