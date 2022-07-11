FROM python:3.8-buster


WORKDIR /usr/mithrandir/django_project

COPY ./requirements.txt  /usr/mithrandir/requirements.txt

RUN pip install -r /usr/mithrandir/requirements.txt

COPY . /usr/mithrandir/django_project


EXPOSE 8000

CMD ['python3', 'manage.py', 'runserver', '0.0.0.0:8000']