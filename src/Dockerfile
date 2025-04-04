FROM python:3.11
WORKDIR /workspace
COPY src/requirements.txt .
RUN pip install -r requirements.txt

COPY ./alembic ./alembic
COPY ./alembic.ini ./
COPY ./src ./src

CMD uvicorn src.main:app --host 0.0.0.0