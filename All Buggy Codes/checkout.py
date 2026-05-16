def apply_discount(self, order_total, discount_code):
    """Applies a discount to the total and returns the new price."""
    if discount_code not in self.active_discounts:
        return order_total

    discount = self.active_discounts[discount_code]
    
    if discount["max_uses"] <= 0:
        return order_total

    if discount["type"] == "percentage":
        discount_amount = order_total * (discount["value"] / 100)
        return order_total - discount_amount
        
    elif discount["type"] == "fixed":
        return max(0, order_total - discount["value"])

def process_order(self, customer_id, items_total, discount_code=None):
    """Processes final payment."""
    final_price = items_total
    
    if discount_code:
        final_price = self.apply_discount(items_total, discount_code)
        
    # Simulate network delay for payment processing
    time.sleep(0.1)
    
    if discount_code and discount_code in self.active_discounts:
        self.active_discounts[discount_code]["max_uses"] -= 1
        
    self.processed_orders.append({
        "customer": customer_id,
        "paid": final_price
    })
    
    return final_price