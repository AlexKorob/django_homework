import time
from django.shortcuts import render
from .models import Test, Testrun, Question, TestrunAnswer
from django.db.models import Q
from .forms import QuestionForm, TestForm, TestrunAnswerForm
from notes.models import Note
from django.contrib.contenttypes.models import ContentType

from .utils import ObjectCreateMixin, ObjectUpdateMixin
from notes.utils import NoteCreateMixin
from django.views.generic import View, ListView


def index(request):
    search_query = request.GET.get("search", '')
    if search_query:
        # Q(title__icontains=search_query) - "i" указывает на регистронезависимый поиск
        tests = Test.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query),
                                    status=Test.PUBLISHED)
    else:
        tests = Test.objects.filter(status=Test.PUBLISHED)
    return render(request, "questions/index.html", context={"tests": tests})


def test_detail(request, test_id):
    test = Test.objects.get(id=test_id)
    questions = Question.objects.filter(tests__id=test_id)
    content_type = ContentType.objects.get_for_model(test)
    notes = Note.objects.filter(note_item__content_type=content_type, note_item__object_id=test.id)
    return render(request, "questions/test_detail.html", context={"test": test, "questions": questions, "notes": notes})


class TestAddNotes(NoteCreateMixin, View):
    app_label = "questions"
    model = "test"
    template_name = "questions/add_notes.html"


def testrun(request, test_id):
    num_quest = Question.objects.filter(tests__id=test_id).count()
    questions = Question.objects.filter(tests__id=test_id)

    if request.method == "GET":
        formset = []
        for i in range(num_quest):
            formset.append(TestrunAnswerForm())

        data = zip(formset, questions)
        context = {"test_id": test_id, "data": data}
        return render(request, "questions/test.html", context=context)

    if request.method == "POST":
        formset = []
        if "name" not in request.POST:
            name = str(time.time()).replace(".", "_")

        testrun = Testrun.objects.create(test_id=test_id, name=name)

        for i in range(num_quest):
            form = TestrunAnswerForm(request.POST["answer-" + str(questions[i].id)])
            formset.append(form)

        for form in formset:
            if len(form.data) <= 0:
                errors = []
                errors.append("Не все поля заполнены!")
                data = zip(formset, questions)
                context = {"test_id": test_id, "data": data, "errors": errors}
                testrun.delete()
                return render(request, "questions/test.html", context=context)

        for i in range(num_quest):
            testrun_answer = TestrunAnswer.objects.create(testrun=testrun,
                                                          question_id=questions[i].id,
                                                          answer=formset[i].data)
            testrun_answer.save()
        return render(request, "questions/success.html")


class TestrunAddNotes(NoteCreateMixin, View):
    app_label = "questions"
    model = "testrun"
    template_name = "questions/add_notes.html"


def testrun_list(request):
    testruns = Testrun.objects.all().order_by("-id")
    return render(request, "questions/testrun_list.html", context={"testruns": testruns})


def testrun_detail(request, id):
    testrun = TestrunAnswer.objects.filter(testrun_id=id).select_related("question")
    content_type = ContentType.objects.get_by_natural_key(app_label="questions", model="testrun")
    notes = Note.objects.filter(note_item__content_type=content_type, note_item__object_id=id)
    return render(request, "questions/testrun_detail.html", context={"testrun": testrun,
                                                                     "notes": notes,
                                                                     "testrun_id": id})


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
