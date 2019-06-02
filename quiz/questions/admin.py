from django.contrib import admin
from questions.models import Testrun, Test, Question, TestrunAnswer


class TestAdmin(admin.ModelAdmin):
    pass


class QuestionAdmin(admin.ModelAdmin):
    pass


class TestrunAdmin(admin.ModelAdmin):
    pass


class TestrunAnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(TestrunAnswer, TestrunAnswerAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Testrun, TestrunAdmin)
