from typing import Callable
import ollama
from ollama import ResponseError
import os
from dotenv import load_dotenv
from .tools.shopping import shoppingFunctions
from .tools.weather import weatherFunctions
import logging
import sys

load_dotenv()
host = os.getenv("OLLAMA_HOST")

client = ollama.Client(host=host)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("pancake")


class Model:
    def __init__(self, _name: str, _systemPrompt: str = "") -> None:
        self.name = _name
        self.systemPrompt = _systemPrompt


def loadSystemPromptFromFile() -> str:
    try:
        with open("system_prompt.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        print("System prompt file not found, using empty system prompt")
        return ""


system = loadSystemPromptFromFile()

# qwen = Model("qwen3.5:9b", system)
gemma4 = Model("gemma4:e4b", system)

model: Model = gemma4
messages = [{"role": "system", "content": model.systemPrompt}]


# Available Tools
def get_model_info() -> str:
    """Get current model information.

    Returns:
        Model name and system prompt.
    """

    return f"Name: {model.name}, System Prompt: {model.systemPrompt}"


available_functions: dict[str, Callable] = {
    "get_model_info": get_model_info,
}

available_functions.update(shoppingFunctions)
available_functions.update(weatherFunctions)


def chat(message: str) -> str | None:
    messages.append({"role": "user", "content": message})

    try:
        logger.info(f"user: {message}")
        logger.info(f"{model.name}: Thinking...")

        # Get the model's response
        response = client.chat(
            model=model.name,
            messages=messages,
            tools=list(available_functions.values()),
            think=True,
        )

        # Add to context
        messages.append(response.message.model_dump(exclude_none=True))

        tool_calls = response.message.tool_calls or []

        for call in tool_calls:
            name = call.function.name
            args = call.function.arguments or {}
            func = available_functions.get(name)
            try:
                result = func(**args) if func else f"Unknown tool: {name}"
                logger.info(f"Calling tool '{name}' with args '{args}'")
            except Exception as e:
                result = f"Error calling {name}: {e}"
            messages.append(
                {
                    "role": "tool",
                    "content": str(result),
                    "tool_name": name,
                }
            )

        # Return response
        return response.message.content
    except ResponseError as e:
        logger.error("Error: ", e.error)
    except ConnectionError:
        logger.error("Ollama not installed or failed to connect!")


def download_model(tag: str) -> None:
    ollama.pull(tag)
