from django import forms
from .models import Question, Test, TestrunAnswer, Testrun
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', ]
        widgets = {
            'question': forms.TextInput(attrs={'style': 'width: 450px; margin-bottom: 20px;'}),
        }

    def clean_question(self):
        cleaned_data = self.cleaned_data
        if len(cleaned_data["question"]) <= 5:
            raise forms.ValidationError("Вопрос не может состоять менее чем из 5-ти символов!")
        return cleaned_data['question']


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'status', 'questions']

    def clean_title(self):
        cleaned_data = self.cleaned_data
        if len(cleaned_data["title"]) <= 2:
            raise forms.ValidationError("Заголовок не может состоять менее чем из 3-х символов!")
        return cleaned_data['title']

    def clean_questions(self):
        if len(self.cleaned_data["questions"]) == 0:
            raise forms.ValidationError("Тест должен минимум 1 вопрос")
        return self.cleaned_data["questions"]


class TestrunAnswerForm(forms.ModelForm):
    class Meta:
        model = TestrunAnswer
        fields = ["answer", ]

    def clean(self):
        for data in self.cleaned_data.values():
            if len(data) <= 1:
                raise forms.ValidationError("Поле должно быть заполнено")
        return self.cleaned_data


class TestrunForm(forms.ModelForm):
    class Meta:
        model = Testrun
        fields = ["name", "test", "answer"]


class UserCreateForm(UserCreationForm):
    UserCreationForm.error_messages = {
        'password_mismatch': "Пароли не совпадают",
    }

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username):
            raise forms.ValidationError("Такой Логин уже существует")
        elif len(username) <= 2:
            raise forms.ValidationError("Логин не может состоять менее чем из 3-х символов!")
        return username

    def clean_first_name(self):
        if len(self.cleaned_data["first_name"]) <= 2:
            raise forms.ValidationError("Имя не может состоять менее чем из 3-х символов!")
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        if len(self.cleaned_data["last_name"]) <= 2:
            raise forms.ValidationError("Фамилия не может состоять менее чем из 3-х символов!")
        return self.cleaned_data['last_name']
