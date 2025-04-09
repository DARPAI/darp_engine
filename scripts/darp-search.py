#!/usr/bin/env python3
"""
List matching MCP servers from the registry.
"""
import argparse
import json
import sys
from typing import Any
from typing import Dict
from typing import List

import requests

default_registry_url: str = "http://localhost:80"


def main() -> None:
    parser = argparse.ArgumentParser(description="Search for servers in the registry")
    parser.add_argument("query", help="Search query string")
    parser.add_argument(
        "--registry-url",
        default=default_registry_url,
        help=f"Registry URL (default: {default_registry_url})",
    )
    parser.add_argument(
        "--format",
        choices=["names", "fulltext", "json"],
        default="names",
        help="Output format (default: names)",
    )

    args = parser.parse_args()

    servers = search_servers(args.query, args.registry_url)
    display_servers(servers, args.format)


def search_servers(
    query: str, base_url: str = default_registry_url
) -> List[Dict[str, Any]]:
    url = f"{base_url}/servers/search"
    params = {"query": query}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f"Error: Failed to search servers - {error}", file=sys.stderr)
        sys.exit(1)


def display_servers(
    servers: List[Dict[str, Any]], format_output: str = "names"
) -> None:
    if format_output == "json":
        display_servers_json(servers)
    elif format_output == "names":
        display_servers_names(servers)
    elif format_output == "fulltext":
        display_servers_fulltext(servers)


def display_servers_json(servers: List[Dict[str, Any]]) -> None:
    print(json.dumps(servers, indent=2))


def display_servers_names(servers: List[Dict[str, Any]]) -> None:
    print(f"Found {len(servers)} servers:")
    for server in servers:
        print(f"{server['name']}")


def display_servers_fulltext(servers: List[Dict[str, Any]]) -> None:
    print(f"Found {len(servers)} servers:")
    for server in servers:
        print(f"{server['id']}: {server['name']}")
        print(f"{indent(server['url'], 1)}")
        print(f"{indent(server['description'], 1)}")
        if server["tools"]:
            print(indent("Tools:", 1))
        for tool in server["tools"]:
            print(f"{indent(tool['name'], 2)}")
            print(f"{indent(tool['description'], 2)}")
            print(f"{indent(json.dumps(tool['input_schema'], indent=2), 2)}")


def indent(text: str, level: int = 1, prefix: str = "  ") -> str:
    return "\n".join(prefix * level + line for line in text.split("\n"))


if __name__ == "__main__":
    main()
