from django import forms
from .models import Question, Test


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


class TestrunForm(forms.Form):
    def clean(self):
        for data in self.cleaned_data.values():
            if len(data) <= 1:
                raise forms.ValidationError("Поле должно быть заполнено")
        return self.cleaned_data
