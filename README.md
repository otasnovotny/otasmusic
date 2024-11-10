# Otas music

This app was created nearby 2016 when I needed to know what record I've done, when and with whom.

Live demo (beta): [music.otasovo.cz](https://music.otasovo.cz/)

- Clone repo and navigate to the root folder
- Copy `tracks` folder (if any) into `./backend/static/`.

## Database

### Init

Create database
```
docker compose -f compose.dev.yml exec -it db psql -v ON_ERROR_STOP=1 --username otasmusic --dbname otasmusic
```

Run migrations:
```
docker compose -f compose.dev.yml exec -it app python manage.py migrate
```

Create superuser:
```
docker compose -f compose.dev.yml exec -it app python manage.py createsuperuser
```

### Backup
```
docker compose -f compose.dev.yml exec -it db pg_dump -U otasmusic -d otasmusic -f /tmp/otasmusic.psql
```

### Restore
```
docker compose -f compose.dev.yml exec -it db psql -U otasmusic -d otasmusic -f /docker-entrypoint-initdb.d/otasmusic.psql
```

## Run setup `localhost`

For development purposes.
- Install python:3.12.1
- `sudo apt install python3.12-venv`

Prepare virtual env
```
cd ./backend && \
python3.12 -m venv ./.venv && \
source ./.venv/bin/activate && \
pip install --upgrade pip && \
pip install poetry && \
poetry install
cd ..
```

Run database container
```
docker compose -f compose.dev.yml up -d db
```

Run migrations
```
python manage.py migrate
```

Check browser at http://localhost:8000

Check browser at http://localhost:8000/admin

# Run setup `Dockerfile.dev`

For developemnt / testing purposes on Beta server.

Run containers
```
docker compose -f compose.dev.yml up -d --build
```

Run migratiions
```
docker compose -f compose.dev.yml exec -it app python manage.py migrate
```

Collect static files
```
docker compose -f compose.dev.yml exec -it app python manage.py collectstatic
```

Check browser at http://localhost

Check browser at http://localhost/admin