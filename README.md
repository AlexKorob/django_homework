## Quiz site (login)

```bash
  git clone https://github.com/AlexKorob/django_homework.git
  python3 -m venv ./venv
  . venv/bin/activate
  pip3 install -r requirements.txt
  cd quiz
  ./manage.py runserver

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

  superuser:
    login: alex; password: 123

  user:
    login: alex1; password: hello1209
    login: alex2; password: hello1209

  authors:
    login: vasya; password: hello1209
    login: Petro; password: hello1209

  moderator:
    login: Oleg; password: hello1209

```
