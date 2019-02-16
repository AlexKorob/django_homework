## Quiz site Celery

```bash
  git clone https://github.com/AlexKorob/django_homework.git
  python3 -m venv ./venv
  . venv/bin/activate
  pip3 install -r requirements.txt
  cd quiz
  ./manage.py runserver
```
After 3 days created test will deactivate

Run worker
```bash
  celery -A tasks worker -B
```
