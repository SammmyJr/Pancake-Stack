from typing import Callable, Mapping
from discord import Message
import ollama
from ollama import ResponseError
import os
from dotenv import load_dotenv
from .tools.list import listFunctions
from .tools.weather import weatherFunctions
import logging
import sys
from pathlib import Path

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


# load a system prompt from the 'system_prompt.txt' file, return it
def loadSystemPromptFromFile() -> str:
    script_dir = Path(__file__).resolve().parent

    try:
        with open(script_dir / "system_prompt.txt") as file:
            return file.read()
    except FileNotFoundError:
        print("System prompt file not found, using empty system prompt")
        return ""


system = loadSystemPromptFromFile()

# qwen = Model("qwen3.5:9b", system)
gemma4 = Model("gemma4:e4b", system)

# init model
# TODO: Pull message from memory, rather than recreate on run.
model: Model = gemma4
messages = [{"role": "system", "content": model.systemPrompt}]


# Available Tools
def get_model_info() -> str:
    """Get current model information.

    Returns:
        Model name and system prompt.
    """

    return f"Name: {model.name}, System Prompt: {model.systemPrompt}"


# load available functions into the model
# TODO: Add a proper tool loader function.
available_functions: dict[str, Callable] = {
    "get_model_info": get_model_info,
}

available_functions.update(listFunctions)
available_functions.update(weatherFunctions)

MAX_TOOL_ROUNDS = 5


# Add a tool call message
async def add_toolcall(name: str, args: Mapping, statusMessage: Message) -> None:
    status = statusMessage.content + f"\n🛠️ Called tool '{name}' with args: {args}"
    await statusMessage.edit(content=status)


# Chat with the model, use tool calls if needed, return a response.
# TODO: Stream output to Discord via editing messages?
async def chat(message: str, statusMessage: Message) -> str | None:
    messages.append({"role": "user", "content": message})

    try:
        logger.info(f"user: {message}")
        logger.info(f"{model.name}: Thinking...")

        response = None

        for _ in range(MAX_TOOL_ROUNDS):
            # Send full history (incl. prior tool results) back to the model
            response = client.chat(
                model=model.name,
                messages=messages,
                tools=list(available_functions.values()),
                think=True,
            )

            # Add to context
            messages.append(response.message.model_dump(exclude_none=True))

            tool_calls = response.message.tool_calls or []
            if not tool_calls:
                break  # real answer, done

            for call in tool_calls:
                name = call.function.name
                args = call.function.arguments or {}
                func = available_functions.get(name)
                try:
                    result = func(**args) if func else f"Unknown tool: {name}"
                    logger.info(f"Calling tool '{name}' with args '{args}'")
                    await add_toolcall(name, args, statusMessage)
                except Exception as e:
                    result = f"Error calling {name}: {e}"
                messages.append(
                    {
                        "role": "tool",
                        "content": str(result),
                        "tool_name": name,
                    }
                )

        if response is None:
            return None

        if response.message.tool_calls:
            logger.warning("Tool call limit hit, no final answer produced")

        # Return response
        return response.message.content
    except ResponseError as e:
        logger.error("Error: ", e.error)
    except ConnectionError:
        logger.error("Ollama not installed or failed to connect!")


def download_model(tag: str) -> None:
    ollama.pull(tag)
