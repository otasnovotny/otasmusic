#!/bin/bash
#docker compose exec -T db psql -U otasmusic -d otasmusic < ./../../db/otasmusic.psql

docker compose down
sudo rm -r dbdata
docker compose up -d

echo "Waiting for postgres server is up"
until docker compose exec -T db psql -U otasmusic -d otasmusic -c "select 1" > /dev/null 2>&1;
do
  sleep 1
done

echo "Restoring database"
docker compose exec -T postgres_db psql otasmusic otasmusic < ./dbdump/otasmusic.psql
