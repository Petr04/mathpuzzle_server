from rest_framework import serializers

from userapi.serializers import UserDataSerializer
from .models import Task, Question, Answer, Attempt, \
    TextChoiceAttemptAnswer, OrderAttemptAnswer

import random
import json


class AnswerSerializer(serializers.Serializer):
    answer_num = serializers.IntegerField()
    text = serializers.CharField()
    is_true = serializers.BooleanField(write_only=True)


class AttemptSerializer(serializers.Serializer):
    user = UserDataSerializer()
    value = serializers.BooleanField()
    id = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # ret['user'] = UserDataSerializer(instance.user).data

        first_question_id = instance.question.task.questions.earliest('id').id
        current_question_id = instance.question.id
        ret['question_number'] = current_question_id - first_question_id

        if instance.question.type in ('textQuestion', 'choiceQuestion'):
            ret['answer'] = instance.answer.value
        elif instance.question.type == 'orderQuestion':
            ret['answer'] = json.loads(instance.answer.value)

        return ret


class QuestionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=32, allow_blank=True,
        allow_null=True)
    attempts_max = serializers.IntegerField()
    text = serializers.CharField()
    type = serializers.ChoiceField(choices=Question.type_choices)
    id = serializers.IntegerField(read_only=True)
    answers = AnswerSerializer(many=True, write_only=True)
    attempts = AttemptSerializer(many=True, read_only=True)

class ChoiceQuestionSerializer(QuestionSerializer):
    answers = AnswerSerializer(many=True)
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret['answers'] = map(
            lambda answer: answer['text'],
            sorted(ret['answers'], key=lambda answer: answer['answer_num'])
        )

        return ret

class OrderQuestionSerializer(ChoiceQuestionSerializer):
    def to_representation(self, instance):
        ret = QuestionSerializer.to_representation(self, instance)

        ret['answers'] = list(map(
            lambda answer: answer['text'],
            ret['answers']
        ))
        random.shuffle(ret['answers'])

        return ret


class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    check_on_submit = serializers.BooleanField(default=False)
    questions = QuestionSerializer(many=True, allow_null=True)
    author = UserDataSerializer(read_only=True)
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        if request is None:
            raise KeyError('No request object.'
                ' Please provide it through context param.')

        questions_data = validated_data.pop("questions")
        task = Task.objects.create(**validated_data, author=request.user)
        for question_data in questions_data:
            answers_data = question_data.pop("answers")
            question = Question.objects.create(task=task, **question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        return task

    def to_representation(self, instance):
        request = self.context.get('request')
        if request is None:
            raise KeyError('No request object.'
                ' Please provide it through context param.')

        ret = super().to_representation(instance)
        
        if not self.context.get('short'):
            return ret

        for i in range(len(ret["questions"])):
            ret["questions"][i] = ret["questions"][i]["title"]

        ret['status'] = instance.get_status(request.user)

        return ret
