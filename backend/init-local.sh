#!/bin/bash
# install python3.12
sudo apt install python3.12-venv
python3.12 -m venv ./.venv
source ./.venv/bin/activate
pip install poetry
poetry install
# copy .env here