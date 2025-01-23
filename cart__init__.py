import json
from typing import List, Union
from cart import dao
from products import Product, get_product


class Cart:
    """
    Represents a user's shopping cart.
    """
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> 'Cart':
        """
        Loads a Cart object from a dictionary.
        """
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=[get_product(item) for item in json.loads(data['contents'])],
            cost=data['cost']
        )


def get_cart(username: str) -> List[Product]:
    """
    Retrieves the cart for a specific user.

    Args:
        username (str): The username of the user.

    Returns:
        List[Product]: A list of Product objects in the user's cart.
    """
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    products_in_cart = []
    for cart_detail in cart_details:
        contents = json.loads(cart_detail['contents'])
        products_in_cart.extend(get_product(item) for item in contents)

    return products_in_cart


def add_to_cart(username: str, product_id: int) -> None:
    """
    Adds a product to the user's cart.

    Args:
        username (str): The username of the user.
        product_id (int): The ID of the product to add.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    """
    Removes a product from the user's cart.

    Args:
        username (str): The username of the user.
        product_id (int): The ID of the product to remove.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    """
    Deletes the user's cart.

    Args:
        username (str): The username of the user.
    """
    dao.delete_cart(username)
