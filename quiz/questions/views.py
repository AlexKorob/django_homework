from django.shortcuts import render
from django.shortcuts import redirect
from .models import Test, Testrun, Question
from django.db.models import Q
from .forms import QuestionForm


def index(request):
    search_query = request.GET.get("search", '')
    if search_query:
        # Q(title__icontains=search_query) - "i" указывает на регистронезависимый поиск
        tests = Test.objects.filter(Q(title__contains=search_query) | Q(description__contains=search_query),
                                    status=20)
    else:
        tests = Test.objects.filter(status=20)
    return render(request, "questions/index.html", context={"tests": tests})


def test_detail(request, test_id):
    test = Test.objects.get(id=test_id)
    print(test.id)
    question = Question.objects.filter(tests__id=test_id).order_by("id")[0]
    return render(request, "questions/question_detail.html", context={"test": test, "question": question})


def question(request, test_id, question_id):
    questions = list(Question.objects.filter(id__gte=question_id, tests__id=test_id).order_by("id"))
    if len(questions) > 1:
        question = questions[0]
        next_question = True
    else:
        question = questions[0]
        next_question = False
    print(test_id, question_id, next_question)
    context = {"test_id": test_id, "question": question, "next_question": True, "question_id": question.id,}

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            testrun = Testrun.objects.create(answer=form.cleaned_data["answer"],
                                             test_id=test_id,
                                             question_id=question_id)
            testrun.save()
            if next_question != False:
                context["question"] = questions[1]
                context["question_id"] = context["question"].id
                if len(questions) == 2:
                    context["next_question"] = False
                return render(request, "questions/question.html", context=context)
            return redirect("success")

        context["errors"] = form.errors
        return render(request, "questions/question.html", context=context)

    return render(request, "questions/question.html", context=context)


def success(request):
    return render(request, "questions/success.html", {})
