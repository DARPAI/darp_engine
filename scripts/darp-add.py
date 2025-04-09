#!/usr/bin/env python3
"""
Add new MCP servers to the registry
"""
import argparse
import json

import requests

default_registry_url: str = "http://localhost:80"


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a new MCP server to the registry")
    parser.add_argument("--url", required=True, help="Endpoint URL for the server")
    parser.add_argument("--name", required=True, help="Unique server name")
    parser.add_argument("--description", required=True, help="Server description")
    parser.add_argument("--logo", default=None, help="Logo URL")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--registry-url", default=default_registry_url, help="Registry API endpoint URL"
    )

    args = parser.parse_args()

    server_data = {
        "name": args.name,
        "description": args.description,
        "url": args.url,
        "logo": args.logo,
    }

    response = requests.post(f"{args.registry_url}/servers/", json=server_data)
    response.raise_for_status()
    if args.verbose:
        print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()
