import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from  prompts import system_prompt
from functions.get_files_info import available_functions as gaf
from functions.run_python_file import available_functions as raf
import json
from functions.call_function import call_function
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

#openai client initialization
# client = OpenAI(
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#     api_key=api_key,
# )

client = OpenAI(
    base_url=os.environ["LOCAL_LLM_BASE_URL"],
    api_key=os.environ.get("LOCAL_LLM_API_KEY", "lm-studio"),
    timeout=120.0,
    max_retries=2,
)


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]
available_tools = raf + gaf
seen_calls = set()

for _ in range(20):
    response = client.chat.completions.create(
        model=os.environ["LOCAL_LLM_MODEL"],
        messages=messages,
        tools=available_tools,
    )

    internal_message = response.choices[0].message
    messages.append(internal_message)

    if internal_message.tool_calls:
        for tool_call in internal_message.tool_calls:
            call_key = (
                tool_call.function.name,
                tool_call.function.arguments,
            )

            # if call_key in seen_calls:
            #     print("Agent is repeating a tool call. Stopping.")
            #     messages.append({
            #     "role": "user",
            #     "content": (
            #         "You repeated a tool call. Use the results already in the conversation "
            #         "to take a different action or provide your final answer."
            #     ),
            #     })
            #     continue

            # seen_calls.add(call_key)
            result_message = call_function(
                tool_call=tool_call,
                verbose=args.verbose,
            )
            if not result_message["content"]:
                raise Exception("Tool call returned empty content")
            messages.append(result_message)

            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print(f"Response: {internal_message.content}")
        break

    if args.verbose and response.usage:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
else:
    print("Agent stopped: reached the 20-iteration limit.")
    sys.exit(1)