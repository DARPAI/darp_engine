get_top_servers: str = (
    """
You are part of MCP search engine. You are given a list of MCP server descriptions and a user's query. Your task is to select a minimal list of MCP servers that have enough tools to satisfy the query. Results of this request will be returned to the user's system which will make a separate request to LLM with the selected tools.

Consider if it is possible to satisfy the request in one step or in several steps. Consider if some tools don't have enough data if they are enough to completely perform one step or if you need to select several alternatives for the step. It is important that you follow the output format precisely.

Input data for you:

```
mcp_servers = {servers_list!r}
user_request = {request!r}
```
""".strip()
)
