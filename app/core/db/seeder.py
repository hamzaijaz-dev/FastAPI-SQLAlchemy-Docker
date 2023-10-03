from app.core.db.session import SessionLocal
from app.ecommerce.v1.models import Category, Product, Inventory, Customer, Order, OrderItem, InventoryChangeHistory


def seed_items():
    session = SessionLocal()

    try:
        if not session.query(Product).all():

            # Seed Categories
            category1 = Category(name="Category 1")
            category2 = Category(name="Category 2")
            session.add(category1)
            session.add(category2)

            # Seed Products
            product1 = Product(name="Product 1", sku="SKU1", description="Description 1", price=10.99, categories=category1)
            product2 = Product(name="Product 2", sku="SKU2", description="Description 2", price=15.99, categories=category2)
            session.add(product1)
            session.add(product2)

            # Seed Inventory
            inventory1 = Inventory(initial_quantity=100, remaining_quantity=100, threshold=10, products=product1)
            inventory2 = Inventory(initial_quantity=200, remaining_quantity=200, threshold=20, products=product2)
            session.add(inventory1)
            session.add(inventory2)

            # Seed Customers
            customer1 = Customer(name="Customer 1", email="customer1@example.com", phone="1234567890", address="Address 1")
            customer2 = Customer(name="Customer 2", email="customer2@example.com", phone="9876543210", address="Address 2")
            session.add(customer1)
            session.add(customer2)

            # Seed Orders
            order1 = Order(total_amount=25.98, status="confirmed", customers=customer1)
            order2 = Order(total_amount=10.99, status="delivered", customers=customer2)
            session.add(order1)
            session.add(order2)

            # Seed Order Items
            order_item1 = OrderItem(orders=order1, products=product1, quantity=2)
            order_item2 = OrderItem(orders=order2, products=product2, quantity=1)
            session.add(order_item1)
            session.add(order_item2)

            # Seed Inventory Change History
            inventory_change_history1 = InventoryChangeHistory(quantity_change=10, new_quantity=110, product=product1)
            inventory_change_history2 = InventoryChangeHistory(quantity_change=5, new_quantity=205, product=product2)
            session.add(inventory_change_history1)
            session.add(inventory_change_history2)

            session.commit()

    finally:
        session.close()
