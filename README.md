## Quiz site (docker)

```bash
  git clone https://github.com/AlexKorob/django_homework.git
  python3 -m venv ./venv
  . venv/bin/activate
  git checkout django_quiz_docker
  cd quiz
  pip3 install -r requirements.txt
  ./manage.py migrate
  ./manage.py compilemessages
  ./manage.py runserver
```

#### Configuration Postgresql:

```bash
  sudo su - postgres
  psql
  CREATE DATABASE quiz;
  CREATE USER alex WITH PASSWORD '123';
  GRANT ALL PRIVILEGES ON DATABASE quiz TO alex;
  \q
  logout
```

#### Build docker images, create and run containers:
```bash
  docker-compose up
```

#### If you want create superuser:
```bash
  docker-compose run web python3 manage.py createsuperuser
```

#### If you are installing docker on Linux Mint, on during installation you must do that:
```bash
  echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu xenial stable" | \
    sudo tee /etc/apt/sources.list.d/
  apt update
  sudo apt-get install docker-ce docker-ce-cli containerd.io
```
