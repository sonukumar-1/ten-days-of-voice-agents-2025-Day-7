import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.cart import Cart
from src.order_manager import OrderManager

def test_cart_flow():
    print("Testing Cart Flow...")
    cart = Cart()
    
    # Add items
    cart.add_item("item1", "Milk", 5.00, 1)
    cart.add_item("item2", "Bread", 3.00, 2)
    
    print(f"Cart Total (Expected 11.0): {cart.get_total()}")
    assert cart.get_total() == 11.0
    
    # Update quantity
    cart.update_quantity("item2", 1)
    print(f"Cart Total after update (Expected 8.0): {cart.get_total()}")
    assert cart.get_total() == 8.0
    
    # Remove item
    cart.remove_item("item1")
    print(f"Cart Total after remove (Expected 3.0): {cart.get_total()}")
    assert cart.get_total() == 3.0
    
    print("Cart Flow Passed!")

def test_order_flow():
    print("\nTesting Order Flow...")
    cart = Cart()
    cart.add_item("item1", "Pizza", 15.00, 1)
    
    om = OrderManager(orders_dir="test_orders")
    order_id = om.place_order(cart)
    print(f"Order Placed: {order_id}")
    
    saved_order = om.get_order(order_id)
    print(f"Saved Order Total: {saved_order['total']}")
    assert saved_order['total'] == 15.00
    
    # Cleanup
    import shutil
    shutil.rmtree("test_orders")
    print("Order Flow Passed!")

if __name__ == "__main__":
    test_cart_flow()
    test_order_flow()
