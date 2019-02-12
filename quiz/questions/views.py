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


def check_user_in_users_group(user):
    if user.groups.filter(name="users").exists():
        return True
    else:
        raise PermissionDenied()


def check_user_in_authors_group(user):
    if user.groups.filter(name="authors").exists():
        return True
    else:
        raise PermissionDenied()


def index(request):
    search_query = request.GET.get("search", '')
    if search_query:
        # Q(title__icontains=search_query) - "i" указывает на регистронезависимый поиск
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


class TestAddNotes(PermissionRequiredMixin, LoginRequiredMixin, NoteCreateMixin, View):
    permission_required = "questions.test"
    raise_exception = True
    app_label = "questions"
    model = "test"
    template_name = "questions/add_notes.html"


@login_required
# @permission_required("questions.testrun", raise_exception=True)
@user_passes_test(check_user_in_users_group)
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


class TestrunAddNotes(NoteCreateMixin, View):
    app_label = "questions"
    model = "testrun"
    template_name = "questions/add_notes.html"


@login_required
#@permission_required("questions.testrun", raise_exception=True)
@user_passes_test(check_user_in_users_group)
def testrun_list(request):
    name = request.user.username
    permissions = Permission.objects.filter(user=request.user)
    print("PERMISSIONS: ", permissions)
    testruns = Testrun.objects.filter(name=name).order_by("-id")
    return render(request, "questions/testrun_list.html", context={"testruns": testruns})


@login_required
@user_passes_test(check_user_in_users_group)
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

    def dispatch(self, request, *args, **kwargs):
        request.POST["creator"] = request.user.id
        return super().dispatch(request, *args, **kwargs)

class TestUpdate(ObjectUpdateMixin, View):
    model = Test
    form_model = TestForm
    template = "questions/test_update.html"


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
