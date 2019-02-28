from rest_framework import generics
from .serializers import TestSerializer, TestSerializerPOST, QuestionSerializer, TestrunSerializer
from .models import Test, Testrun, TestrunAnswer, Question
from rest_framework import viewsets, permissions
from .permissions import IsOwnerOrReadOnly, CantChange
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializerPOST
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def list(self, request, format=None):
        serializer = TestSerializer(self.queryset, many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, CantChange)
    authentication_classes = (TokenAuthentication, SessionAuthentication)


class TestrunViewSet(viewsets.ModelViewSet):
    queryset = Testrun.objects.all()
    serializer_class = TestrunSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, CantChange)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def perform_create(self, serializer):
        serializer.save(name=self.request.user)
