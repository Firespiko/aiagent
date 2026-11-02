# AI Agent Project

This repository contains a lightweight local AI coding agent that can inspect a project, read and edit files, and run Python scripts through a tool-calling loop. The project is designed to work with a local LLM via an OpenAI-compatible API and uses a small demo application in the `calculator/` directory to show how the agent behaves in practice.

## What this project does

The agent in `main.py`:

- loads environment variables from a `.env` file
- connects to a local model endpoint via `OpenAI`
- sends a system prompt and the user request to the model
- allows the model to call tools such as listing files, reading file contents, writing files, and running Python
- keeps the conversation going until the model produces a final answer or the loop hits a limit

This makes it a minimal autonomous coding assistant for exploring a project and making changes within a controlled working directory.

## Project structure

```text
aiagent/
├── main.py                  # agent runner and tool-calling loop
├── prompts.py               # system prompt used by the agent
├── config.py                # project constants
├── pyproject.toml           # Python project metadata and dependencies
├── README.md                # project overview
├── functions/
│   ├── call_function.py     # dispatches tool calls to the right handler
│   ├── get_files_info.py    # file listing, content reading, and writing helpers
│   └── run_python_file.py   # executes a Python file in a sandboxed directory
├── calculator/              # sample project the agent inspects and works with
│   ├── main.py
│   ├── tests.py
│   ├── README.md
│   └── pkg/
│       ├── calculator.py
│       ├── render.py
│       └── morelorem.txt
├── test_get_file_content.py
├── test_get_files_info.py
├── test_run_python_file.py
└── test_write_file.py
```

## Core agent flow

The runtime flow is driven by `main.py`:

1. The script creates an OpenAI-compatible client using `LOCAL_LLM_BASE_URL` and `LOCAL_LLM_MODEL`.
2. It sends the system prompt from `prompts.py` and the user query.
3. The model may decide to call tools from `functions/`.
4. `call_function.py` maps each tool call to the correct implementation.
5. Results are appended back to the model conversation until the agent has enough information to answer.

## Available tools

The agent can call these functions:

- `get_files_info`: list files and folders relative to the allowed working directory
- `get_file_content`: read a file safely within the working directory
- `write_file`: create or overwrite a file within the working directory
- `run_python_file`: execute a Python file and capture its output

The tool layer restricts access to the `calculator/` directory, preventing reads or writes outside the project scope.

## Sample project

The sample app under `calculator/` is a small expression evaluator:

- `calculator/main.py` parses command-line input and evaluates expressions
- `calculator/pkg/calculator.py` implements arithmetic evaluation with precedence handling
- `calculator/tests.py` verifies addition, subtraction, multiplication, division, and error cases

This sample project is intended to let the agent demonstrate file inspection and code execution in a realistic, bounded environment.

## Setup

1. Create a virtual environment if desired.
2. Install the project dependencies:

```bash
pip install -e .
```

This installs the packages declared in `pyproject.toml`, including `openai` and `python-dotenv`.

3. Create a `.env` file with your local model settings, for example:

```env
LOCAL_LLM_BASE_URL=http://localhost:1234/v1
LOCAL_LLM_MODEL=local-model-name
LOCAL_LLM_API_KEY=lm-studio
```

The code also looks for `GEMINI_API_KEY`, but the main execution path is configured for a local LLM service.

## Run the agent

Example:

```bash
python main.py "Inspect the calculator project and explain how the expression evaluator works."
```

For more verbose tool tracing:

```bash
python main.py "Inspect the calculator project and explain how the expression evaluator works." --verbose
```

## Run the sample project directly

```bash
python calculator/main.py "3 + 5 * 2"
```

This should print a structured result using the calculator package.

## Testing

The repository includes a few focused test scripts to validate the tool layer:

- `test_get_file_content.py`
- `test_get_files_info.py`
- `test_run_python_file.py`
- `test_write_file.py`

These scripts exercise the safety checks and function behavior for reading, listing, running, and writing files.

## Notes

This project is intentionally small and educational: it is a compact example of a tool-using LLM agent that can work inside a sandboxed file tree. It is suitable for experimenting with local-model orchestration, tool calling, and secure file access patterns.
