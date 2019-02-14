import time
from django.shortcuts import render
from .models import Test, Testrun, Question, TestrunAnswer
from django.db.models import Q
from .forms import QuestionForm, TestForm, TestrunAnswerForm, UserCreateForm
from notes.models import Note
from django.shortcuts import reverse, redirect
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType

from .utils import ObjectCreateMixin, ObjectUpdateMixin
from notes.utils import NoteCreateMixin
from django.views.generic import View, ListView
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied


def index(request):
    search_query = request.GET.get("search", '')
    if search_query:
        if request.user.groups.filter(name="authors").exists():
            # Q(title__icontains=search_query) - "i" указывает на регистронезависимый поиск
            tests = Test.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query),
                                    status=Test.PUBLISHED, creator_id=request.user.id)
        else:
            tests = Test.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query),
                                        status=Test.PUBLISHED)
    else:
        if request.user.groups.filter(name="authors").exists():
            tests = Test.objects.filter(status=Test.PUBLISHED, creator_id=request.user.id)
        else:
            tests = Test.objects.filter(status=Test.PUBLISHED)

    return render(request, "questions/index.html", context={"tests": tests})


@login_required
def test_detail(request, test_id):
    test = Test.objects.get(id=test_id)
    questions = Question.objects.filter(tests__id=test_id)
    content_type = ContentType.objects.get_for_model(test)
    notes = Note.objects.filter(note_item__content_type=content_type, note_item__object_id=test.id)
    return render(request, "questions/test_detail.html", context={"test": test, "questions": questions, "notes": notes})


class TestAddNotes(LoginRequiredMixin, PermissionRequiredMixin, NoteCreateMixin, View):
    permission_required = "questions.add_test"
    raise_exception = True
    app_label = "questions"
    model = "test"
    template_name = "questions/add_notes.html"

    def get(self, request, id):
        test = Test.objects.get(id=id)
        if request.user.id != test.creator_id:
            raise PermissionDenied()
        return NoteCreateMixin.get(self, request, id)


@login_required
@permission_required("questions.add_testrun", raise_exception=True)
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
        name = request.user.username
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


class TestrunAddNotes(LoginRequiredMixin, PermissionRequiredMixin, NoteCreateMixin, View):
    app_label = "questions"
    model = "testrun"
    template_name = "questions/add_notes.html"
    raise_exception = True
    permission_required = "questions.change_testrun"


@login_required
@permission_required("questions.view_testrun", raise_exception=True)
def testrun_list(request):
    if request.user.groups.filter(name="moderators"):
        testruns = Testrun.objects.all().order_by("-id")
    else:
        name = request.user.username
        testruns = Testrun.objects.filter(name=name).order_by("-id")
    return render(request, "questions/testrun_list.html", context={"testruns": testruns})


@login_required
@permission_required("questions.view_testrun", raise_exception=True)
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


class QuestionCreate(LoginRequiredMixin, PermissionRequiredMixin, ObjectCreateMixin, View):
    form_model = QuestionForm
    template = "questions/question_create.html"
    raise_exception = True
    permission_required = "questions.add_question"


class QuestionUpdate(LoginRequiredMixin, PermissionRequiredMixin, ObjectUpdateMixin, View):
    model = Question
    form_model = QuestionForm
    template = "questions/question_update.html"
    permission_required = "questions.change_question"
    raise_exception = True


class TestCreate(LoginRequiredMixin, PermissionRequiredMixin, ObjectCreateMixin, View):
    form_model = TestForm
    template = "questions/test_create.html"
    raise_exception = True
    permission_required = "questions.add_test"

    def post(self, request):
        bound_form = self.form_model(request.POST)

        if bound_form.is_valid():
            test = Test.objects.create(title=bound_form.cleaned_data["title"],
                                       description=bound_form.cleaned_data["description"],
                                       creator=request.user,
                                       status=bound_form.cleaned_data["status"])
            print("BOUND_FORM: ", bound_form.cleaned_data["questions"])
            test.questions.set([quest for quest in bound_form.cleaned_data["questions"]])
            return redirect(test)
        else:
            return render(request, self.template, {'form': bound_form, "errors": bound_form.errors})


class TestUpdate(LoginRequiredMixin, PermissionRequiredMixin, ObjectUpdateMixin, View):
    model = Test
    form_model = TestForm
    template = "questions/test_update.html"
    raise_exception = True
    permission_required = "questions.change_test"

    def get(self, request, id):
        test = Test.objects.get(id=id)
        if request.user.id == test.creator_id or request.user.groups.filter(name="moderators").exists():
            return ObjectUpdateMixin.get(self, request, id)
        else:
            raise PermissionDenied()


class UserCreate(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("list_tests"))
        form = UserCreateForm()
        return render(request, "questions/login/register.html", context={"form": form})

    def post(self, request):
        bound_form = UserCreateForm(request.POST)

        if bound_form.is_valid():
            bound_form.save()
            user = authenticate(username=bound_form.cleaned_data["username"], password=bound_form.cleaned_data["password2"])
            if request.POST["user"] == "user":
                group = Group.objects.get(name="users")
                group.user_set.add(user)
            elif request.POST["user"] == "author":
                group = Group.objects.get(name="authors")
                group.user_set.add(user)
            login(request, user)
            return HttpResponseRedirect(reverse("list_tests"))
        return render(request, "questions/login/register.html", context={"form": bound_form, "errors": bound_form.errors})


class UserAuthentication(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("list_tests"))
        form = AuthenticationForm()
        return render(request, "questions/login/login.html", context={"form": form})

    def post(self, request):
        bound_form = AuthenticationForm(request=request, data=request.POST)
        if bound_form.is_valid():
            user = authenticate(username=bound_form.cleaned_data["username"], password=bound_form.cleaned_data["password"])
            login(request, user)
            return HttpResponseRedirect(reverse("list_tests"))
        error = list(bound_form.errors.values())[0]
        return render(request, "questions/login/login.html", context={"form": bound_form, "error": error})

class UserLogout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("list_tests"))
