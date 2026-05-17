import json
from typing import Dict, Any

class InventoryManager:
    def __init__(self):
        # Master inventory database (mocked as a dictionary for this test)
        self.master_inventory = {
            "SKU-1001": {"name": "Wireless Mouse", "stock": 50, "price": 25.99},
            "SKU-1002": {"name": "Mechanical Keyboard", "stock": 15, "price": 89.99},
            "SKU-1003": {"name": "USB-C Cable", "stock": 100, "price": 12.50},
        }
        self.sync_logs = []

    def get_item(self, sku: str) -> Dict[str, Any]:
        """Returns the current data for a specific SKU."""
        return self.master_inventory.get(sku, {})

    def _validate_payload(self, item_data: Dict[str, Any]) -> bool:
        """Ensure the incoming payload has the minimum required fields."""
        if "sku" not in item_data:
            return False
        return True

    def process_supplier_sync(self, supplier_name: str, payload_json: str) -> bool:
        """
        Processes a batch update from a supplier via webhooks.
        Suppliers send JSON arrays of items to update stock and prices.
        """
        try:
            items = json.loads(payload_json)
        except json.JSONDecodeError:
            self.sync_logs.append(f"[{supplier_name}] Failed to parse JSON payload.")
            return False

        processed_count = 0
        
        for item in items:
            if not self._validate_payload(item):
                continue

            sku = item["sku"]
            
            # If item doesn't exist, create it if it has all required fields
            if sku not in self.master_inventory:
                if "name" in item and "price" in item and "stock" in item:
                    self.master_inventory[sku] = {
                        "name": item["name"],
                        "stock": item["stock"],
                        "price": item["price"]
                    }
                    processed_count += 1
                continue

            # Update existing item
            current_item = self.master_inventory[sku]
            
            # Update price if a valid new price is provided
            new_price = item.get("price")
            if new_price and new_price > 0:
                current_item["price"] = new_price

            # Update stock levels

            new_stock = item.get("stock")
            if new_stock: 
                current_item["stock"] = new_stock

            processed_count += 1

        self.sync_logs.append(f"[{supplier_name}] Successfully processed {processed_count} items.")
        return True