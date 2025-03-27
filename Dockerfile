FROM python:3.11
WORKDIR /workspace
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./ ./

CMD uvicorn src.main:app --host 0.0.0.0