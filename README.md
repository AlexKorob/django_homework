## Quiz site (login)

```bash
  git clone https://github.com/AlexKorob/django_homework.git
  python3 -m venv ./venv
  . venv/bin/activate
  pip3 install -r requirements.txt
  cd quiz
  ./manage.py runserver
```

Permissions authors:
  * create questions
  * create tests
  * change own tests
  * add notes to test
  * delete own tests
  * search own tests

Permissions users:
  * pass any testrun
  * see own passed testruns

Permissions moderators:
  * change any test
  * delete any test
  * add notes to testrun


#### For correct permission, registration and authorization, create three groups with necessary permissions above:
 * authors
 * users
 * moderators
