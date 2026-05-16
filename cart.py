class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, name, quantity):
        self.items.append({"name": name, "qty": quantity})
        return True

    def get_total_items(self):
        return sum(item["qty"] for item in self.items)

# Made with Bob
