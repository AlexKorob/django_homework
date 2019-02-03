from django.db import models

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
    status = models.SmallIntegerField(choices=STATUS, default=STATUS_DRAFT)
    questions = models.ManyToManyField("Question", related_name="tests")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    class Meta:
       ordering = ['-created_on']

    def __str__(self):
       return self.title


class Question(models.Model):
    question = models.CharField(max_length=200)
    true_answer = models.TextField(blank=True)

    def __str__(self):
        return self.question


class Testrun(models.Model):
    name = models.CharField(max_length=40, blank=True)
    test = models.ForeignKey(Test, related_name='testrun', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='testrun', on_delete=models.CASCADE)
    answer = models.TextField(max_length=500, error_messages={"required": "Поле ответа не может быть пустым"})

    def __str__(self):
        return str(self.id) + " | " + str(self.name) + " | " + str(self.test)
