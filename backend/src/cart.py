from typing import List, Dict, Optional
import json
from dataclasses import dataclass, asdict

@dataclass
class CartItem:
    id: str
    name: str
    price: float
    quantity: int
    notes: str = ""

    @property
    def total(self) -> float:
        return self.price * self.quantity

class Cart:
    def __init__(self):
        self.items: Dict[str, CartItem] = {}

    def add_item(self, item_id: str, name: str, price: float, quantity: int = 1, notes: str = "") -> CartItem:
        if item_id in self.items:
            self.items[item_id].quantity += quantity
            if notes:
                self.items[item_id].notes = f"{self.items[item_id].notes}, {notes}".strip(", ")
        else:
            self.items[item_id] = CartItem(id=item_id, name=name, price=price, quantity=quantity, notes=notes)
        return self.items[item_id]

    def remove_item(self, item_id: str) -> Optional[CartItem]:
        return self.items.pop(item_id, None)

    def update_quantity(self, item_id: str, quantity: int) -> Optional[CartItem]:
        if item_id in self.items:
            if quantity <= 0:
                return self.remove_item(item_id)
            self.items[item_id].quantity = quantity
            return self.items[item_id]
        return None

    def get_total(self) -> float:
        return sum(item.total for item in self.items.values())

    def clear(self):
        self.items.clear()

    def to_dict(self) -> Dict:
        return {
            "items": [asdict(item) for item in self.items.values()],
            "total": self.get_total()
        }

    def __str__(self) -> str:
        if not self.items:
            return "Your cart is empty."
        
        lines = ["Here is what you have in your cart:"]
        for item in self.items.values():
            note_str = f" ({item.notes})" if item.notes else ""
            lines.append(f"- {item.quantity}x {item.name}{note_str}: ${item.total:.2f}")
        lines.append(f"Total: ${self.get_total():.2f}")
        return "\n".join(lines)
