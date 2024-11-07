FROM python:3.12

RUN apt-get update
RUN apt-get install vim -y

ENV POETRY_VIRTUALENVS_CREATE 0
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/backend
COPY ./../.env ./
COPY ./../backend/pyproject.toml ./

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install

# TODO Otas port
CMD 'poetry' 'run' 'gunicorn' 'config.wsgi:application' '-b' ':8000' '--reload'
