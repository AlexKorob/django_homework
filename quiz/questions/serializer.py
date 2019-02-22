from rest_framework import serializers
from .models import Test, Question, Testrun, TestrunAnswer


class TestSerializer(serializers.ModelSerializer):
    # creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'creator', 'questions']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question']


class TestrunSerializer(serializers.ModelSerializer):
    # name = serializers.ReadOnlyField(source='name.username')

    class Meta:
        model = Testrun
        fields = ['id', 'name', 'test', 'answer']


class TestrunAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestrunAnswer
        fields = ['id', 'testrun', 'question', 'answer']
