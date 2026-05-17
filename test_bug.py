import pytest
from decimal import Decimal
import sys
import os

# Add the directory containing the buggy code to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'All Buggy Codes'))

from invoice_calculator import InvoiceCalculator


def test_prorated_refund_exact_total_match():
    """
    Test case from bug report: 3 T-shirts at $10 each, $10 flat refund.
    The sum of refund_applied must EXACTLY equal $10.00, not $9.99.
    """
    calculator = InvoiceCalculator()
    
    # Setup: 3 identical T-shirts at $10 each
    order_lines = [
        {"id": "item1", "price": 10.0, "quantity": 1},
        {"id": "item2", "price": 10.0, "quantity": 1},
        {"id": "item3", "price": 10.0, "quantity": 1}
    ]
    
    refund_amount = 10.0
    
    # Execute
    processed_refunds = calculator.calculate_prorated_refund(order_lines, refund_amount)
    
    # Verify: Sum of refund_applied must EXACTLY match requested refund
    total_refund_applied = sum(item['refund_applied'] for item in processed_refunds)
    
    # Critical assertion: Must be exactly $10.00, not $9.99
    assert total_refund_applied == refund_amount, (
        f"Refund total mismatch: applied ${total_refund_applied} but requested ${refund_amount}. "
        f"Lost ${refund_amount - total_refund_applied} to rounding!"
    )
    
    # Verify audit function also passes
    assert calculator.verify_total_refund(processed_refunds, refund_amount), (
        "verify_total_refund audit function failed"
    )
    
    # Additional check: Each item should get approximately $3.33
    for refund in processed_refunds:
        assert 3.33 <= refund['refund_applied'] <= 3.34, (
            f"Item {refund['item_id']} refund ${refund['refund_applied']} is outside expected range"
        )


def test_prorated_refund_with_different_prices():
    """
    Test with varying item prices to ensure remainder distribution works generally.
    """
    calculator = InvoiceCalculator()
    
    order_lines = [
        {"id": "item1", "price": 15.0, "quantity": 1},
        {"id": "item2", "price": 25.0, "quantity": 1},
        {"id": "item3", "price": 10.0, "quantity": 1}
    ]
    
    refund_amount = 7.0
    
    processed_refunds = calculator.calculate_prorated_refund(order_lines, refund_amount)
    total_refund_applied = sum(item['refund_applied'] for item in processed_refunds)
    
    assert total_refund_applied == refund_amount, (
        f"Refund total mismatch: applied ${total_refund_applied} but requested ${refund_amount}"
    )
    
    assert calculator.verify_total_refund(processed_refunds, refund_amount)


def test_prorated_refund_single_item():
    """
    Edge case: Single item should get the full refund amount.
    """
    calculator = InvoiceCalculator()
    
    order_lines = [
        {"id": "item1", "price": 50.0, "quantity": 1}
    ]
    
    refund_amount = 20.0
    
    processed_refunds = calculator.calculate_prorated_refund(order_lines, refund_amount)
    
    assert processed_refunds[0]['refund_applied'] == refund_amount
    assert calculator.verify_total_refund(processed_refunds, refund_amount)

# Made with Bob
