## Quiz site (celery)

```bash
  git clone https://github.com/AlexKorob/django_homework.git
  python3 -m venv ./venv
  . venv/bin/activate
  pip3 install -r requirements.txt
  git checkout django_quiz_celery
  cd quiz
  ./manage.py runserver
```

After 3 days created test will deactivate

Start worker (in new terminal)

```bash
  . venv/bin/activate
  cd quiz
  celery -A questions worker -B --loglevel=INFO
```
