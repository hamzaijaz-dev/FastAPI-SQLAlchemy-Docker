from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger
from typing import List, Dict, Union
from sqlalchemy.orm import joinedload, Session
from sqlalchemy import func

from app.core.db.session import get_db
from app.ecommerce.v1.models import Category, Product, Order, OrderItem, Inventory, InventoryChangeHistory
from app.ecommerce.v1.schema import CategorySchema, ProductSchema

router = APIRouter()


@router.get("/overview", status_code=200)
async def get_overview_details(db: Session = Depends(get_db)):
    """
    Get all orders from the database.
    """

    orders = db.query(Order).options(
        joinedload(Order.customers),
        joinedload(Order.order_items).joinedload(OrderItem.products)
    ).all()

    sales_data = []
    for order in orders:
        sales_data.append({
            'order_id': order.id,
            'total_amount': order.total_amount,
            'status': order.status,
            'customer': {
                'id': order.customers.id,
                'name': order.customers.name,
                'email': order.customers.email,
                'phone': order.customers.phone,
                'address': order.customers.address,
            },
            'order_items': [
                {
                    'product_id': item.products.id,
                    'product_name': item.products.name,
                    'quantity': item.quantity,
                }
                for item in order.order_items
            ],
            'created_at': order.created_at,
        })

    return sales_data


@router.get("/sales-details", response_model=List[Dict[str, Union[int, float]]], status_code=200)
async def get_sales_details(
    db: Session = Depends(get_db),
    start_date: date = Query(None, description="Start date of the date range"),
    end_date: date = Query(None, description="End date of the date range"),
    product_id: int = Query(None, description="Product ID to filter by product"),
    category_id: int = Query(None, description="Category ID to filter by category"),
):
    """
    Provide sales data by date range, product, and category.
    """
    sales_query = db.query(
        OrderItem.product_id,
        func.sum(OrderItem.quantity).label("total_quantity"),
        func.sum(Product.price * OrderItem.quantity).label("total_sale_amount"),
    ).join(OrderItem.products).join(Product.categories)

    if start_date and end_date:
        sales_query = sales_query.filter(
            func.date(OrderItem.orders.created_at).between(start_date, end_date)
        )

    if product_id:
        sales_query = sales_query.filter(OrderItem.product_id == product_id)

    if category_id:
        sales_query = sales_query.filter(Category.id == category_id)

    sales_query = sales_query.group_by(OrderItem.product_id, Category.id)
    sales_data = sales_query.all()

    sales_data_dict = [
        {
            "product_id": row[0],
            "total_quantity": row[1],
            "total_sales": row[2]
        }
        for row in sales_data
    ]

    return sales_data_dict


@router.get("/inventory-details", status_code=200)
async def get_inventory_details(db: Session = Depends(get_db)):
    """
    Get all inventory details from the database and check for low stock items.
    """
    inventory = db.query(Inventory).options(joinedload(Inventory.products)).all()
    low_stock_threshold = 10  # general threshold to alert for all products
    low_stock_items = []

    for item in inventory:
        if item.remaining_quantity <= low_stock_threshold:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                low_stock_items.append({
                    "product_id": item.product_id,
                    "product_name": product.name,
                    "remaining_quantity": item.remaining_quantity,
                    "threshold": item.threshold
                })

    return {
        "inventory": inventory,
        "low_stock_items": low_stock_items
    }


@router.get("/categories", status_code=200)
async def get_categories(db: Session = Depends(get_db)):
    """
    Get all categories from the database.
    """
    categories = db.query(Category).all()
    return categories


@router.post("/categories", status_code=201)
async def create_category(payload: CategorySchema, db: Session = Depends(get_db)):
    """
    Create a new category in the database.
    """
    db_category = Category(**payload.dict())
    db.add(db_category)
    db.commit()
    logger.success("Created a category.")
    return db_category


@router.put("/categories/{category_id}", status_code=200)
async def update_category(category_id: int, payload: CategorySchema, db: Session = Depends(get_db)):
    """
    Update a category in the database by its ID.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in payload.dict().items():
        setattr(category, key, value)

    db.commit()
    logger.success("Updated a category.")
    return category


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category from the database by its ID.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    logger.success("Deleted a category.")
    return {"message": "Category deleted successfully"}


@router.get("/products", status_code=200)
async def get_products(db: Session = Depends(get_db)):
    """
    Get all products from the database.
    """
    products = db.query(Product).all()
    return products


@router.post("/products", status_code=201)
async def create_product(payload: ProductSchema, db: Session = Depends(get_db)):
    """
    Create a new product in the database.
    """
    if db.query(Category).filter(Category.id == payload.category_id).first():
        db_product = Product(**payload.dict())
        db.add(db_product)
        db.commit()
        logger.success("Created a product.")
        return db_product
    else:
        raise HTTPException(status_code=404, detail="Category not found")


@router.put("/products/{product_id}", status_code=200)
async def update_product(product_id: int, payload: ProductSchema, db: Session = Depends(get_db)):
    """
    Update a product in the database by its ID.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in payload.dict().items():
        setattr(product, key, value)

    db.commit()
    logger.success("Updated a product.")
    return product


@router.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product from the database by its ID.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    logger.success("Deleted a product.")
    return {"message": "Product deleted successfully"}


@router.put("/update-inventory/{product_id}", status_code=200)
async def update_inventory(product_id: int, quantity_change: int, db: Session = Depends(get_db)):
    """
    Update inventory levels for a specific product and track the change.
    """
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()

    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")

    # Calculate new remaining quantity after the change
    new_remaining_quantity = inventory.remaining_quantity + quantity_change

    if new_remaining_quantity < 0:
        raise HTTPException(status_code=400, detail="Inventory cannot go negative")

    # Update the remaining quantity and track the change
    inventory.remaining_quantity = new_remaining_quantity

    # Create a history record to track the change
    change_history = InventoryChangeHistory(
        product_id=product_id,
        quantity_change=quantity_change,
        new_quantity=new_remaining_quantity,
        change_timestamp=datetime.now()
    )

    db.add(change_history)
    db.commit()
    db.refresh(inventory)

    return {"message": "Inventory updated successfully"}


@router.get("/inventory-change-history/{product_id}", status_code=200)
async def get_inventory_change_history(product_id: int, db: Session = Depends(get_db)):
    """
    Get the change history for a specific product's inventory.
    """
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    change_history = db.query(InventoryChangeHistory).filter(InventoryChangeHistory.product_id == product_id).all()

    return {"product_name": product.name, "change_history": change_history}
