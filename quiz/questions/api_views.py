from rest_framework import generics
from .serializer import TestSerializer, QuestionSerializer, TestrunSerializer, TestrunAnswerSerializer
from .models import Test, Testrun, TestrunAnswer, Question


class TestList(generics.ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class TestrunList(generics.ListCreateAPIView):
    queryset = Testrun.objects.all()
    serializer_class = TestrunSerializer

    def perform_create(self, serializer):
        serializer.save(name=self.request.user)


class TestrunDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Testrun.objects.all()
    serializer_class = TestrunSerializer


class TestrunAnswerList(generics.ListAPIView):
    queryset = TestrunAnswer.objects.all()
    serializer_class = TestrunAnswerSerializer
