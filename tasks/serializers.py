from rest_framework import serializers

from .models import Task, Question, Answer


class AnswerSerializer(serializers.Serializer):
    answer_num = serializers.IntegerField()
    text = serializers.CharField()

class PostAnswerSerializer(AnswerSerializer):
    is_true = serializers.BooleanField()

class QuestionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=32, allow_blank=True, allow_null=True)
    attempts = serializers.IntegerField()
    text = serializers.CharField()
    type = serializers.ChoiceField(choices=Question.type_choices)


class PostQuestionSerializer(QuestionSerializer):
    answers = PostAnswerSerializer(many=True)

class GetQuestionSerializer(QuestionSerializer):
    id = serializers.IntegerField()

class GetChoiceQuestionSerializer(GetQuestionSerializer):
    answers = AnswerSerializer(many=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['answers'] = map(
            lambda answer: answer['text'],
            sorted(ret['answers'], key=lambda answer: answer['answer_num'])
        )
        return ret


class TaskSerializerNoQuestions(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    check_on_submit = serializers.BooleanField(default=False)

    def create(self, validated_data):
        questions_data = validated_data.pop("questions")
        task = Task.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop("answers")
            question = Question.objects.create(task=task, **question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)
        return task

class PostTaskSerializer(TaskSerializerNoQuestions):
    questions = PostQuestionSerializer(many=True, allow_null=True)

class GetTaskSerializer(PostTaskSerializer):
    id = serializers.IntegerField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for i in range(len(ret["questions"])):
            ret["questions"][i] = ret["questions"][i]["title"]
        return ret
