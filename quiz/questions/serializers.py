from rest_framework import serializers
from .models import Test, Question, Testrun, TestrunAnswer
from django.contrib.auth.models import User
from notes.models import NoteItem, Note


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question')


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'name')


class TestSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    questions = QuestionSerializer(many=True)
    notes = NoteSerializer(many=True)

    class Meta:
        model = Test
        fields = ('id', 'title', 'description', 'creator', 'questions', 'notes')


class TestSerializerPOST(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Test
        fields = ('id', 'title', 'description', 'creator', 'questions', 'notes')


class TestrunAnswerSerializer(serializers.ModelSerializer):
    question = serializers.CharField(source='question.question')

    class Meta:
        model = TestrunAnswer
        fields = ('id', 'question', 'answer')


class TestrunSerializer(serializers.ModelSerializer):
    name = UserSerializer(read_only=True)
    test = TestSerializer(read_only=True)
    answer = TestrunAnswerSerializer(many=True, source="testrun_answer")
    notes = NoteSerializer(many=True)

    class Meta:
        model = Testrun
        fields = ('id', 'name', 'test', 'answer', 'notes')


class NoteTargetField(serializers.ModelSerializer):
    serializer_map = {"Test": TestSerializer, "Testrun": TestrunSerializer}

    def to_representation(self, obj):
        serializer = self.serializer_map[obj.__class__]
        return serializer.to_representation(obj)


class NoteItemSerializer(serializers.ModelSerializer):
    note = NoteSerializer()
    content_object = NoteTargetField()

    class Meta:
        model = NoteItem
        fields = ('id', 'note', 'content_object')
