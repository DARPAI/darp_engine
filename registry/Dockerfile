FROM python:3.11
WORKDIR /workspace
COPY registry/requirements.txt .
RUN pip install -r requirements.txt

COPY alembic ./alembic
COPY alembic.ini ./alembic.ini
COPY registry ./registry
ENV PATH "$PATH:/workspace/registry/scripts"
