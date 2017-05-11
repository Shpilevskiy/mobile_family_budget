FROM python:3.6

ADD ./requirements.txt /api/requirements.txt
ADD ./docker-entrypoint.sh /api/

WORKDIR /api/
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' apiuser

WORKDIR /api/mobile_family_budget/
ENTRYPOINT ["/api/docker-entrypoint.sh"]