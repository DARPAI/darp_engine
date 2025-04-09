FROM python:3.11
WORKDIR /workspace
COPY mcp_server/requirements.txt .
RUN pip install -r requirements.txt

COPY mcp_server ./mcp_server
ENV PATH "$PATH:/workspace/mcp_server/scripts"