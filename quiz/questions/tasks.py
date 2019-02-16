from celery import shared_task
from .models import Test


@shared_task
def add(x, y):
    return x + y


@shared_task
def task_block_test(id):
    test = Test.objects.get(id=id)
    test.blocked = True
    test.save()
    return f"{test} Test with id={test.id} has blocked"
