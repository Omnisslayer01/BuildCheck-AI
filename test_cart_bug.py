import pytest
from cart import ShoppingCart


def test_negative_quantity_should_raise_error():
    """
    Test that adding an item with negative quantity raises ValueError.
    Bug Report #992: Cart accepts negative quantities when it should reject them.
    """
    cart = ShoppingCart()
    
    # This should raise ValueError but currently doesn't (the bug)
    with pytest.raises(ValueError):
        cart.add_item("Widget", -5)


def test_zero_quantity_should_raise_error():
    """
    Test that adding an item with zero quantity raises ValueError.
    Quantities should be at least 1.
    """
    cart = ShoppingCart()
    
    with pytest.raises(ValueError):
        cart.add_item("Widget", 0)


def test_positive_quantity_should_work():
    """
    Test that adding an item with positive quantity works correctly.
    This is the expected behavior.
    """
    cart = ShoppingCart()
    result = cart.add_item("Widget", 5)
    
    assert result is True
    assert cart.get_total_items() == 5


def test_multiple_items_total():
    """
    Test that multiple valid items are totaled correctly.
    """
    cart = ShoppingCart()
    cart.add_item("Widget", 10)
    cart.add_item("Gadget", 5)
    
    assert cart.get_total_items() == 15

# Made with Bob
