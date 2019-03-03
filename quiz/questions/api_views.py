from rest_framework import generics
from .serializers import (TestSerializer, TestCreateSerializer, QuestionSerializer,
                         TestrunSerializer, UserSerializer)
from .models import Test, Testrun, TestrunAnswer, Question
from rest_framework import viewsets, permissions
from .permissions import IsCreatorOrReadOnly
from .permissions import IsCreatorOrReadOnly as IsUserOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=("get",))
    def tests(self, request, *args, **kwargs):
        user = self.get_object()
        tests = Test.objects.filter(creator=user)
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=("get",))
    def testruns(self, request, *args, **kwargs):
        user = self.get_object()
        testruns = Testrun.objects.filter(user=user)
        serializer = TestrunSerializer(testruns, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=("get",))
    def questions(self, request, *args, **kwargs):
        user = self.get_object()
        questions = Question.objects.filter(creator=user)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TestSerializer
        return TestCreateSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TestrunViewSet(viewsets.ModelViewSet):
    queryset = Testrun.objects.all()
    serializer_class = TestrunSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
