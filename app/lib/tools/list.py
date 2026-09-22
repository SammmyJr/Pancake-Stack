from typing import Callable
from pathlib import Path
import json
import os

script_dir = Path(__file__).resolve().parent


# Load the shopping list file, otherwise create one
def loadLists() -> dict:
    try:
        with open(script_dir / "memory/lists.json", "r") as file:
            return json.loads(file.read())
    except (FileNotFoundError, json.JSONDecodeError):
        Path(script_dir / "memory/lists.json").write_text(json.dumps({}))
        return {}


def saveLists(lists: dict) -> None:
    with open(script_dir / "memory/lists.json.temp", "w") as tempFile:
        tempFile.write(json.dumps(lists))

    os.replace(script_dir / "memory/lists.json.temp", script_dir / "memory/lists.json")


lists = loadLists()


def get_all_lists() -> dict:
    """Get all lists.

    Returns:
        A dict of all lists.
    """

    return lists


def create_list(name: str) -> None:
    """Add a new list.

    Input:
        The name of the new list.
    """

    lists[name] = []
    saveLists(lists)


def remove_list(name: str) -> None:
    """Removes a list.

    Input:
        The name of the list to remove.
    """

    lists.pop(name, None)
    saveLists(lists)


def add_to_list(name: str, item: str):
    """Adds an item to the list.

    Input:
        The name of the list and the item to add.
    """

    try:
        lists[name].append(item)
    except KeyError:
        print(f"List '{name}' not found!")

    saveLists(lists)


def remove_from_list(name: str, item: str):
    """Remove an item from a list.

    Input:
        The name of the list and the item to remove.
    """

    try:
        lists[name].remove(item)
    except KeyError:
        print(f"List '{name}' not found!")

    saveLists(lists)


listFunctions: dict[str, Callable] = {
    "get_all_lists": get_all_lists,
    "create_list": create_list,
    "remove_list": remove_list,
    "add_to_list": add_to_list,
    "remove_from_list": remove_from_list,
}
