from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .models import Test, Testrun, Question
from django.db.models import Q
from .forms import QuestionForm


def index(request):
    search_query = request.GET.get("search", '')
    if search_query:
        # Q(title__icontains=search_query) - "i" указывает на регистронезависимый поиск
        tests = Test.objects.filter(Q(title__contains=search_query) | Q(description__contains=search_query),
                                    status=Test.PUBLISHED)
    else:
        tests = Test.objects.filter(status=Test.PUBLISHED)
    return render(request, "questions/index.html", context={"tests": tests})


def test_detail(request, test_id):
    test = Test.objects.get(id=test_id)
    return render(request, "questions/question_detail.html", context={"test": test})


def questions(request, test_id):
    return HttpResponseNotFound("<h2>This page wasn't created, yet</h2>")


def success(request):
    return render(request, "questions/success.html", {})
