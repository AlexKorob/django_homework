## Quiz site (channels)

```bash
  git clone https://github.com/AlexKorob/django_homework.git
  python3 -m venv ./venv
  . venv/bin/activate
  pip3 install -r requirements.txt
  git checkout django_quiz_channels
  cd quiz
  ./manage.py migrate
  ./manage.py compilemessages
  ./manage.py runserver
```

Before send not safe-method you need add header to request:
  * Authorization: Token <user_token_authentication>

#### Description:
  When some user created Test, users who stand on home-page will be reload
