#!/usr/bin/env bash

set -e

pip install --upgrade -r requirements.txt
alembic upgrade head
uvicorn --reload --proxy-headers --host 0.0.0.0 --port $UVICORN_PORT registry.src.main:app
