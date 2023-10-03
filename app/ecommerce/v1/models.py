
from sqlalchemy import Column, DECIMAL, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.session import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    products = relationship('Product', back_populates='categories')

    def __str__(self):
        return self.name


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    sku = Column(String(255))
    description = Column(Text)
    price = Column(DECIMAL(10, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship('Category', back_populates='products')

    inventory = relationship('Inventory', back_populates='products')
    order_items = relationship('OrderItem', back_populates='products')
    inventory_change_history = relationship('InventoryChangeHistory', back_populates='product')

    def __str__(self):
        return self.name


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    initial_quantity = Column(Integer)
    remaining_quantity = Column(Integer)
    threshold = Column(Integer)

    product_id = Column(Integer, ForeignKey('products.id'))
    products = relationship('Product', back_populates='inventory')


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(255), unique=True, index=True)
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    orders = relationship('Order', back_populates='customers')

    def __str__(self):
        return self.name


class InventoryChangeHistory(Base):
    __tablename__ = 'inventory_change_history'

    id = Column(Integer, primary_key=True, index=True)
    quantity_change = Column(Integer, nullable=False)
    new_quantity = Column(Integer, nullable=False)
    change_timestamp = Column(DateTime(timezone=True), server_default=func.now())

    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship('Product', back_populates='inventory_change_history')

    def __str__(self):
        return f"Inventory Change #{self.id} for Product ID {self.product_id}"


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    total_amount = Column(DECIMAL(precision=2), default=0)

    STATUS_CHOICES = Enum('pending', 'confirmed', 'delivered', name='status')
    status = Column(STATUS_CHOICES, default='pending', nullable=False)

    customer_id = Column(Integer, ForeignKey('customers.id'))
    customers = relationship('Customer', back_populates='orders')

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order_items = relationship('OrderItem', back_populates='orders')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    orders = relationship('Order', back_populates='order_items')
    products = relationship('Product', back_populates='order_items')
