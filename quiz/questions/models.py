from django.db import models
from django.shortcuts import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from notes.models import NoteItem, Note
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Test(models.Model):
    DRAFT = 10
    PUBLISHED = 20
    REJECTED = 30

    STATUS = [
       (DRAFT, "draft"),
       (PUBLISHED, "published"),
       (REJECTED, "rejected")
    ]

    title = models.CharField(max_length=40)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test")
    status = models.SmallIntegerField(choices=STATUS, default=DRAFT)
    questions = models.ManyToManyField("Question", related_name="tests")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    blocked = models.BooleanField(null=True, default=False)
    note = GenericRelation(NoteItem)

    class Meta:
        ordering = ['-created_on']

    def notes(self):
        notes = Note.objects.filter(note_item__content_type=ContentType.objects.get_for_model(self.__class__),
                                    note_item__object_id=self.id)
        return notes

    def get_absolute_url(self):
        return reverse("list_tests")

    def __str__(self):
        return self.title


class Question(models.Model):
    question = models.CharField(max_length=200)
    true_answer = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse("questions_show")


class Testrun(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="testrun", null=True)
    test = models.ForeignKey(Test, related_name='testruns', on_delete=models.CASCADE)
    answer = models.ManyToManyField(Question, related_name="testruns", through="TestrunAnswer")
    note = GenericRelation(NoteItem)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.user) + " | " + str(self.test)

    def notes(self):
        notes = Note.objects.filter(note_item__content_type=ContentType.objects.get_for_model(self.__class__),
                                    note_item__object_id=self.id)
        return notes

    def get_absolute_url(self):
        return reverse("tests_show")


class TestrunAnswer(models.Model):
    testrun = models.ForeignKey(Testrun, on_delete=models.CASCADE, related_name='testrun_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="testrun_answer")
    answer = models.CharField(max_length=120)

    def __str__(self):
        return str(self.testrun) + " | " + str(self.question) + " | " + str(self.answer)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Test)
def create_test(sender, instance=None, created=False, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("notifications", {"type": "send.msg",
                                                                  "message": "reload"})
