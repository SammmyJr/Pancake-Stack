from typing import Callable


shopping = ["bread", "butter", "eggs"]


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


def remove_item_shopping_list(item: str) -> None:
    """Removes an item from the shopping list

    Input:
        The string of the item to be removed.
    """

    shopping.remove(item)


shoppingFunctions: dict[str, Callable] = {
    "get_shopping_list": get_shopping_list,
    "add_item_shopping_list": add_item_shopping_list,
    "remove_item_shopping_list": remove_item_shopping_list,
}
