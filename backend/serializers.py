from rest_framework import serializers

from .models import Task, TextQuestion, ChoiceQuestion, Answer

class QuestionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=32, allow_blank=True, allow_null=True)
    question_num = serializers.IntegerField()
    attempts = serializers.IntegerField()
    text = serializers.CharField()

    class Meta:
        abstract = True


class AnswerSerializer(serializers.Serializer):
    text = serializers.CharField()
    is_true = serializers.BooleanField()


class TextQuestionSerializer(QuestionSerializer):
    answer = serializers.CharField(max_length=32)


class ChoiceQuestionSerializer(QuestionSerializer):
    answers = AnswerSerializer(many=True)

class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64)
    check_on_submit = serializers.BooleanField(default=False)
    text_questions = TextQuestionSerializer(many=True, allow_null=True)
    choice_questions = ChoiceQuestionSerializer(many=True, allow_null=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for i in range(len(ret["text_questions"])):
            ret["text_questions"][i] = ret["text_questions"][i]["title"]

        for i in range(len(ret["choice_questions"])):
            ret["choice_questions"][i] = ret["choice_questions"][i]["title"]

        return ret

    def create(self, validated_data):
        text_questions_data = validated_data.pop("text_questions")
        choice_questions_data = validated_data.pop("choice_questions")

        task = Task.objects.create(**validated_data)
        for text_question_data in text_questions_data:
            TextQuestion.objects.create(task=task, **text_question_data)
        for choice_question_data in choice_questions_data:
            answers_data = choice_question_data.pop("answers")
            question = ChoiceQuestion.objects.create(task=task, **choice_question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)
        return task


