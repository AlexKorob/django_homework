from django.contrib import admin
from questions.models import Testrun, Test, Question


class TestAdmin(admin.ModelAdmin):
    pass


class QuestionAdmin(admin.ModelAdmin):
    pass


class TestrunAdmin(admin.ModelAdmin):
    pass


admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Testrun, TestrunAdmin)
