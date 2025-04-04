FROM python:3.11
WORKDIR /workspace
COPY mcp_server/requirements.txt .
RUN pip install -r requirements.txt

COPY mcp_server ./mcp_server

CMD python3 -m mcp_server.src.main