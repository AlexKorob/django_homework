import time
from django.shortcuts import render
from .models import Test, Testrun, Question
from django.db.models import Q
from .forms import QuestionForm, TestForm, TestrunForm

from .utils import ObjectCreateMixin, ObjectUpdateMixin
from django.views.generic import View, ListView


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
    return render(request, "questions/test_detail.html", context={"test": test})


def testrun(request, test_id):
    num_quest = Question.objects.filter(tests__id=test_id).count()
    questions = Question.objects.filter(tests__id=test_id)

    if request.method == "GET":
        formset = []
        for i in range(num_quest):
            formset.append(TestrunForm())

        data = zip(formset, questions)
        context = {"test_id": test_id, "data": data}
        return render(request, "questions/test.html", context=context)

    if request.method == "POST":
        formset = []
        for i in range(num_quest):
            form = TestrunForm(request.POST["answer-" + str(questions[i].id)])
            formset.append(form)

        for form in formset:
            if len(form.data) <= 0:
                errors = []
                errors.append("Не все поля заполнены!")
                data = zip(formset, questions)
                print("form.errors:", errors)
                context = {"test_id": test_id, "data": data, "errors": errors}
                return render(request, "questions/test.html", context=context)

        if "name" not in request.POST:
            name = str(time.time()).replace(".", "_")

        for i in range(num_quest):
            test = Testrun.objects.create(name=name,
                                          test_id=test_id,
                                          question_id=questions[i].id,
                                          answer=formset[i].data)
            test.save()
        return render(request, "questions/success.html")


def testrun_list(request):
    objects = Testrun.objects.exclude(name="")
    testruns = []
    list_with_names = []

    for object in objects:
        if object.name not in list_with_names:
            list_with_names.append(object.name)
            testruns.append(object)

    return render(request, "questions/testrun_list.html", context={"testruns": testruns})


def testrun_detail(request, name):
    testruns = Testrun.objects.filter(name=name).order_by("id")
    return render(request, "questions/testrun_detail.html", context={"testruns": testruns})


class QuestionListView(ListView):
    model = Question
    template_name = "questions/question_show.html"
    context_object_name = "questions"


class QuestionCreate(ObjectCreateMixin, View):
    form_model = QuestionForm
    template = "questions/question_create.html"


class QuestionUpdate(ObjectUpdateMixin, View):
    model = Question
    form_model = QuestionForm
    template = "questions/question_update.html"


class TestListView(ListView):
    model = Test
    template = "questions/tests.html"
    context_object_name = "test"


class TestCreate(ObjectCreateMixin, View):
    form_model = TestForm
    template = "questions/test_create.html"


class TestUpdate(ObjectUpdateMixin, View):
    model = Test
    form_model = TestForm
    template = "questions/test_update.html"
