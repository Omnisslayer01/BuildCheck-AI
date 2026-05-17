from typing import List, Dict, Any

class InvoiceCalculator:
    def __init__(self):
        self.tax_rate = 0.08  # 8% tax

    def calculate_prorated_refund(self, order_lines: List[Dict[str, Any]], refund_amount: float) -> List[Dict[str, Any]]:
        """
        Distributes a flat refund amount across multiple order lines proportionally
        based on the line item's price.
        """
        total_order_value = sum(item['price'] * item['quantity'] for item in order_lines)
        
        if refund_amount > total_order_value:
            raise ValueError("Refund cannot exceed total order value.")
        if refund_amount <= 0:
            raise ValueError("Refund must be greater than zero.")

        processed_refunds = []
        
        for item in order_lines:
            line_total = item['price'] * item['quantity']
            proportion = line_total / total_order_value
            
            prorated_refund = round(refund_amount * proportion, 2)
            
            processed_refunds.append({
                "item_id": item['id'],
                "original_line_total": line_total,
                "refund_applied": prorated_refund,
                "tax_refunded": round(prorated_refund * self.tax_rate, 2)
            })

        # Fix rounding errors: distribute remainder to last item
        total_applied = sum(item['refund_applied'] for item in processed_refunds)
        remainder = round(refund_amount - total_applied, 2)
        
        if remainder != 0 and processed_refunds:
            processed_refunds[-1]['refund_applied'] = round(
                processed_refunds[-1]['refund_applied'] + remainder, 2
            )
            # Recalculate tax for the adjusted item
            processed_refunds[-1]['tax_refunded'] = round(
                processed_refunds[-1]['refund_applied'] * self.tax_rate, 2
            )

        return processed_refunds

    def verify_total_refund(self, processed_refunds: List[Dict[str, Any]], requested_refund: float) -> bool:
        """Audit function to ensure our math matches reality exactly."""
        total_applied = sum(item['refund_applied'] for item in processed_refunds)
        return round(total_applied, 2) == round(requested_refund, 2)