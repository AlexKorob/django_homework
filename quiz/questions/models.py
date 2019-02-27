from django.db import models
from django.shortcuts import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from notes.models import NoteItem


class Test(models.Model):
    STATUS_DRAFT = 10
    PUBLISHED = 20
    REJECTED = 30

    STATUS = [
       (STATUS_DRAFT, "draft"),
       (PUBLISHED, "published"),
       (REJECTED, "rejected")
    ]

    title = models.CharField(max_length=40)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test")
    status = models.SmallIntegerField(choices=STATUS, default=STATUS_DRAFT)
    questions = models.ManyToManyField("Question", related_name="tests")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    note = GenericRelation(NoteItem)

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return reverse("list_tests")

    def __str__(self):
        return self.title


class Question(models.Model):
    question = models.CharField(max_length=200)
    true_answer = models.TextField(blank=True)

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse("questions_show")


class Testrun(models.Model):
    name = models.CharField(max_length=40, blank=True)
    test = models.ForeignKey(Test, related_name='testruns', on_delete=models.CASCADE)
    answer = models.ManyToManyField(Question, related_name="testruns", through="TestrunAnswer")
    note = GenericRelation(NoteItem)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.name) + " | " + str(self.test)

    def get_absolute_url(self):
        return reverse("tests_show")


class TestrunAnswer(models.Model):
    testrun = models.ForeignKey(Testrun, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="testrun_answer")
    answer = models.CharField(max_length=120)

    def __str__(self):
        return str(self.testrun) + " | " + str(self.question) + " | " + str(self.answer)
