#!/usr/bin/env bash

set -e

pip install --upgrade -r ./requirements.txt
python3 -m mcp_server.src.main
