# DARPEngine
The searchengine for MCP

[![X][x-image]][x-url]
[![Code style: black][black-image]][black-url]
[![Imports: reorder-python-imports][imports-image]][imports-url]
[![Pydantic v2][pydantic-image]][pydantic-url]
[![pre-commit][pre-commit-image]][pre-commit-url]
[![License MIT][license-image]][license-url]

DARPEngine stores metadata for MCP servers hosted online and provides smart search capabilites.

## Features

* Simple CLI
* API access to search
* MCP tool to retrieve search results for connecting manually
* Routing MCP tool based on the server: answer any question using the tools found for the user's request

### Coming soon

* Support for `.well-known/mcp.json`
* Crawler
* Nice frontend
* Hosted version
* Validate different levels of SSL certificates and integrate this info smarly to make sensitive MCP servers difficult to spoof

## Installation

```
export OPENAI_API_KEY=sk-...
docker network create highkey_network
docker compose build
docker compose -f docker-compose.yaml -f docker-compose-debug.yaml up --build --wait
```

## Getting started

You can connect the DARPEngine to an MCP Client (e.g. Claude Desktop or Cursor) using mcp tools provided. Just select SSE mode & specify `http://localhost:4689/sse` as the endpoint.


### Direct CLI use

Another way is to use CLI. Most of the scripts work with just standard Python libraries, but routing tool requires mcp package, you can install script requirements like this:

```
conda create -n darp 'python>=3.10'
conda activate darp
pip install -r mcp_server/requirements.txt
```

When installation is over we can use the scripts.

To begin with it we need to add some MCP servers to the engine, e.g:

```
$ python scripts/darp-add.py --url http://memelabs.ai:3006/sse --name code_analysis --description "Analyze gitlab repo for quality, topics, packages use"
```

Then we can make the requests:

```
$ python scripts/darp-search.py "Analyze https://github.com/BenderV/autochat"
Found 1 servers:
code_analysis
```

You can get more useful results with the routing tool:

```
$ python scripts/darp-router.py "Analyze https://github.com/BenderV/autochat"
assistant: [tool_calls]
[tool] ...
[tool] ...
[tool] ...
assistant:
  ### Code Quality
  The code in the AutoChat repository demonstrates a good level of quality concerning **readability**, **maintainability**, and adherence to best practices:

  - **Readability**: Consistent naming conventions are evident, with adherence to Python's PEP 8 styling guidelines. Descriptive function and variable names enhance the understanding of the code's purpose.

  - **Maintainability**: The code is structured to allow easy updates and modifications, with a clear separation of concerns observed through the use of classes and methods handling distinct functionalities.

  - **Best Practices**: Extensive use of exception handling, type annotations, and docstrings reflect best practices in Python development. Some TODO comments suggest areas for improvement, indicating that further attention is needed.

  ### Code Structure
  The code is organized into multiple files and modules, each serving a distinct purpose:

  - **Modular Design**: Various classes (e.g., `Autochat`, `Image`, `Message`) indicate a well-structured object-oriented design that promotes separation of concerns, making the code easier to navigate.

  - **Logical Organization**: Files are logically separated based on functionality. For example, `chat.py` focuses on chat-related logic, while `model.py` handles message and image processing. The utility functions in `utils.py` enhance reusability.

  - **Testing**: The presence of a test file (`tests/test_utils.py`) shows commitment to testing, crucial for code reliability. The use of `unittest` indicates a structured approach to testing individual components.

  ### Main Functionality
  The code appears to be part of an **AutoChat package**, providing a framework for building conversational agents. Key functionalities include:

  - **Chat Management**: The `Autochat` class acts as the main interface for managing conversations, handling message history, context, and interaction limits.

  - **Message Handling**: Classes like `Message` and `MessagePart` enable structured message creation and processing, accommodating different message types, including text and images.

  - **Functionality Extensions**: Methods like `add_tool` and `add_function` allow dynamic addition of tools and functions, facilitating customization of the chat experience.

  - **Provider Integration**: Different API provider integrations (e.g., OpenAI, Anthropic) are encapsulated within respective classes, allowing flexibility in backend communication.

  - **Utilities**: Utility functions offer additional capabilities such as CSV formatting and function parsing that support main chat operations.

  Overall, the codebase is well-organized and showcases a thoughtful approach to developing a conversational AI framework. There is room for further refinement and enhancement, particularly in documentation and clarity of variable names.

  ### Library Usage
  The project makes use of **AI libraries**, indicated by its functionality related to conversational agents and integration with AI service providers. This supports its ability to manage interactions with AI models efficiently.

  ### Summary
  The AutoChat project is a chat system designed for communication with various AI models, primarily through the `Autochat` class, which manages conversations and supports complex message types, including text and images. The code is moderately complex due to its integration with external APIs and its ability to handle diverse interactions through extensible methods like `add_tool` and `add_function`. The quality of code is commendable, featuring a well-structured modular design that promotes readability and maintainability, although some areas require further documentation and refinement, such as clarifying variable names and enhancing comments. The organization into separate files for models, utilities, and tests aids development, but the utility functions could benefit from better categorization for improved clarity.
```

Of course, the usefulness of the result depends on the MCP servers you connect to the engine.


## Get help and support

Please feel free to connect with us using the [discussion section](https://github.com/hipasus/darp_engine/discussions).

## Contributing

Please read [Contributing to Docling](https://github.com/docling-project/docling/blob/main/CONTRIBUTING.md) for details.

Follow us on X: https://x.com/DARP_AI

## License

The DARPEngine codebase is under MIT license.

<br>

[x-image]: https://img.shields.io/twitter/follow/DARP_AI?style=social
[x-url]: https://x.com/DARP_AI
[black-image]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[imports-image]: https://img.shields.io/badge/%20imports-reorder_python_imports-%231674b1?style=flat&labelColor=ef8336
[imports-url]: https://github.com/asottile/reorder-python-imports/
[pydantic-image]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json
[pydantic-url]: https://pydantic.dev
[pre-commit-image]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[pre-commit-url]: https://github.com/pre-commit/pre-commit
[license-image]: https://img.shields.io/github/license/DARP_AI/darp_engine
[license-url]: https://opensource.org/licenses/MIT
