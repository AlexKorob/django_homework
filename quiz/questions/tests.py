from django.test import TestCase
from .models import Test, Question, Testrun
from django.shortcuts import reverse


class TestrunTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.question_1 = Question.objects.create(question="Тестовый вопрос №1")
        cls.question_2 = Question.objects.create(question="Тестовый вопрос №2")
        cls.test = Test.objects.create(title="Test", status=20, description="Description")
        cls.test.questions.set([cls.question_1, cls.question_2])

    def test_testrun_pass(self):
        url = reverse("test", kwargs={"test_id": self.test.id})
        questions = Question.objects.filter(tests__id=self.test.id)
        post_parameters = {}

        for i in range(questions.count()):
            key = "answer-" + str(questions[i].id)
            post_parameters[key] = "answ"

        client = self.client.post(url, post_parameters)
        self.assertEqual(client.status_code, 200)
        self.assertEqual(Testrun.objects.count(), 1)

    def test_testrun_fail(self):
        url = reverse("test", kwargs={"test_id": self.test.id})
        post_parameters = {"answer-1": "", "answer-2": ""}
        client = self.client.post(url, post_parameters)
        self.assertEqual(client.status_code, 200)
        self.assertEqual(Testrun.objects.count(), 0)


class TestTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.question_1 = Question.objects.create(question="Тестовый вопрос №1")
        cls.question_2 = Question.objects.create(question="Тестовый вопрос №2")

    def test_create_test(self):
        url = reverse("test_create")
        post_parameters = {"title": "Test", "description": "Description",
                           "status": 20, "questions": [self.question_1.id, self.question_2.id]}
        client = self.client.post(url, post_parameters)
        self.assertEqual(client.status_code, 302)
        self.assertEqual(Test.objects.count(), 1)

    def test_create_test_fail(self):
        url = reverse("test_create")
        post_parameters = {"title": "T", "description": "Description",
                           "status": 20, "questions": [self.question_1.id, self.question_2.id]}
        client = self.client.post(url, post_parameters)
        self.assertEqual(client.status_code, 200)
        self.assertEqual(Test.objects.count(), 0)
        post_parameters["title"] = "Title"
        post_parameters["questions"] = ""
        client = self.client.post(url, post_parameters)
        self.assertEqual(Test.objects.count(), 0)

    def test_add_question(self):
        parameters = {"title": "Test", "status": 20, "description": "Description"}
        test = Test.objects.create(**parameters)
        test.questions.add(self.question_1)

        url = reverse("test_update", kwargs={"id": test.id})
        parameters["update"] = True
        parameters["questions"] = [self.question_1.id, self.question_2.id, ]
        client = self.client.post(url, parameters)

        self.assertEqual(client.status_code, 302)
        self.assertEqual(test.questions.count(), 2)
