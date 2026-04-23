from tools import code_n_execute, google_search
import json
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")
url = os.getenv("URL")

client = OpenAI(base_url=url, api_key=api_key)
CODER_MODEL = "qwen/qwen3-coder-480b-a35b-instruct"


def handle_tool_calls(message):
    responses = []
    for tool_call in message.tool_calls:
        if tool_call.function.name == "code_n_execute":
            print("Code n Execute Tool called")
            prompt = json.loads(tool_call.function.arguments)["prompt"]
            result = code_n_execute(prompt, client, CODER_MODEL)
            responses.append(
                {"role": "tool", "content": str(result), "tool_call_id": tool_call.id}
            )
        if tool_call.function.name == "google_search":
            print("Google Search Tool called")
            query = json.loads(tool_call.function.arguments)["query"]
            result = google_search(query)
            responses.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id,
                }
            )
    return responses
