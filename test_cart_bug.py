"""
Test for Customer Issue #992: Shopping cart accepts negative quantities
"""
import pytest
from cart import ShoppingCart


def test_negative_quantity_should_raise_error():
    """Test that adding negative quantity raises ValueError"""
    cart = ShoppingCart()
    
    # This should raise ValueError for negative quantity
    with pytest.raises(ValueError):
        cart.add_item("Apple", -5)


def test_zero_quantity_should_raise_error():
    """Test that adding zero quantity raises ValueError"""
    cart = ShoppingCart()
    
    # This should raise ValueError for zero quantity
    with pytest.raises(ValueError):
        cart.add_item("Banana", 0)


def test_positive_quantity_should_work():
    """Test that positive quantities work correctly"""
    cart = ShoppingCart()
    
    # This should work fine
    result = cart.add_item("Orange", 5)
    assert result == True
    assert cart.get_total_items() == 5


def test_negative_quantity_affects_total():
    """Demonstrate the bug: negative quantities subtract from total"""
    cart = ShoppingCart()
    cart.add_item("Apple", 10)
    cart.add_item("Banana", -5)  # BUG: This should fail but doesn't
    
    # Currently returns 5 (10 + -5), demonstrating the bug
    total = cart.get_total_items()
    assert total == 5  # This passes, showing the bug exists

# Made with Bob
