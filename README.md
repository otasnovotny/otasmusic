# Otas music

This app was created nearby 2016 when I needed to know what record I've done, when and with whom.

Currently it's running on [music.otasovo.cz](https://music.otasovo.cz/).

Clone repo and navigate to the root folder

## Pure `localhost` approach

For development purposes
- Install python:3.12.1
- `sudo apt install python3.12-venv`

### Prepare virtual env
```
cd ./backend && \
python3.12 -m venv ./.venv && \
source ./.venv/bin/activate && \
pip install --upgrade pip && \
pip install poetry && \
poetry install && \
cd ..
```

### Prepare database

Copy db dump file into `./dbdump` folder and run database container
```
docker compose up -d db
```

# `Dockerfile.dev` approach
Run containers
```
docker compose -f compose.dev.yml up -d --build
```

Collect static files
```
docker compose -f compose.dev.yml exec -it app python manage.py collectstatic
```

Check browser at http://localhost