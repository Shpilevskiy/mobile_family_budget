FROM python:3.5

ADD ./requirements.txt /api/requirements.txt
ADD ./docker-entrypoint.sh /api/

WORKDIR /api/
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' apiuser

WORKDIR /api/mobile_family_budget/
RUN python manage.py makemigrations
RUN python manage.py migrate
ENTRYPOINT ["/api/docker-entrypoint.sh"]