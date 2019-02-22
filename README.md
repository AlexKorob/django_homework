## Quiz site (API)

```bash
  git clone https://github.com/AlexKorob/django_homework.git
  python3 -m venv ./venv
  . venv/bin/activate
  pip3 install -r requirements.txt
  git checkout django_quiz_localization
  cd quiz
  ./manage.py migrate
  ./manage.py compilemessages
  ./manage.py runserver
```
