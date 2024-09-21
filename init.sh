#!/bin/bash

git pull git@github.com:otasnovotny/otasmusic.git
# copy dbdump/otasmusic.psql into ./dbdump/
# copy / create secrets (./backend/.env, ./db.env...)
# copy /tracks into ./backend/otasmusic/static/
docker compose up -d

# == local ==
# install python3.12
sudo apt install python3.12-venv
python3.12 -m venv ./.venv
source ./.venv/bin/activate
pip install poetry
poetry install
# copy .env here

# == production ==
docker compose exec -it django_app bash
python manage.py collectstatic
