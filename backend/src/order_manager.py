import json
import os
from datetime import datetime
from typing import Dict, Any
from .cart import Cart

class OrderManager:
    def __init__(self, orders_dir: str = "orders"):
        self.orders_dir = orders_dir
        os.makedirs(self.orders_dir, exist_ok=True)

    def place_order(self, cart: Cart, customer_info: Dict[str, Any] = None) -> str:
        if not cart.items:
            raise ValueError("Cart is empty")

        order_data = {
            "order_id": f"ORD-{int(datetime.now().timestamp())}",
            "timestamp": datetime.now().isoformat(),
            "customer_info": customer_info or {},
            "items": cart.to_dict()["items"],
            "total": cart.get_total(),
            "status": "placed"
        }

        filename = f"{self.orders_dir}/{order_data['order_id']}.json"
        with open(filename, "w") as f:
            json.dump(order_data, f, indent=2)
        
        return order_data["order_id"]

    def get_order(self, order_id: str) -> Dict[str, Any]:
        filename = f"{self.orders_dir}/{order_id}.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return None
