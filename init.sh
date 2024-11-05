#!/bin/bash

# == out of project folder ==

# clone repository
git clone ssh://git@otasovo.cz/~/codebase/otasmusic.git otasmusic

# copy db-dump to server (run from local machine and this folder)
scp ./dbdump/otasmusic.psql otas@motofoko.cz:~/dockerized/otasmusic/dbdump/

# copy static files to server
# scp -r ./static/ otas@motofoko.cz:~/dockerized/otasmusic/backend/otasmusic/static/
scp -r ./static/ otas@motofoko.cz:~/dockerized/otasmusic/backend/

# copy secrets
scp ./secrets/backend/.env.prod otas@motofoko.cz:~/dockerized/otasmusic/backend/.env
scp ./secrets/.env.db otas@motofoko.cz:~/dockerized/otasmusic/

# collect static
docker compose exec -it django_app python manage.py collectstatic

# change otas contact
docker compose exec -it postgres_db psql -U otasmusic -d otasmusic
\dt
update otasmusic_personcontact set contact='otas.novotny@gmail.com' where id=1

# ---
# dump database
docker compose exec -t postgres_db pg_dump -U otasmusic -d otasmusic -f /tmp/otasmusic.sql

# copy database from container to local machine
# docker compose cp postgres_db:/tmp/otasmusic.sql ./my_database_dump.sql

# == local ==
# install python3.12
sudo apt install python3.12-venv
python3.12 -m venv ./.venv
source ./.venv/bin/activate
pip install poetry
poetry install
# copy .env here

# == production ==

