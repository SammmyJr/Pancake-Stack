from typing import Callable
from pathlib import Path

script_dir = Path(__file__).resolve().parent


# Load the shopping list file, otherwise create one
def loadShoppingList() -> list:

    try:
        with open(script_dir / "memory/shopping_list.txt", "r") as file:
            return file.readlines()
    except FileNotFoundError:
        open(script_dir / "memory/shopping_list.txt", "x")
        return loadShoppingList()


def saveShoppingList(shopping: list) -> None:
    with open(script_dir / "memory/shopping_list.txt", "w") as file:
        for item in shopping:
            file.writelines(f"{item}\n")


shopping = loadShoppingList()


def get_shopping_list() -> list:
    """Get items on the shopping list

    Returns:
        A list of items on the shopping list
    """

    return shopping


def add_item_shopping_list(item: str) -> None:
    """Add an item to the shopping list

    Input:
        A string of the new item to be added.
    """

    shopping.append(item)
    saveShoppingList(shopping)


def remove_item_shopping_list(item: str) -> None:
    """Removes an item from the shopping list

    Input:
        The string of the item to be removed.
    """

    shopping.remove(item)
    saveShoppingList(shopping)


shoppingFunctions: dict[str, Callable] = {
    "get_shopping_list": get_shopping_list,
    "add_item_shopping_list": add_item_shopping_list,
    "remove_item_shopping_list": remove_item_shopping_list,
}
