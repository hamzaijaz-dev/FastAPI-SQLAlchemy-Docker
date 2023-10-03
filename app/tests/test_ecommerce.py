from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_sales_details():
    response = client.get("/sales-details")
    assert response.status_code == 200

    response = client.get("/sales-details?start_date=2023-01-01&end_date=2023-12-31&product_id=1&category_id=2")
    assert response.status_code == 200
    sales_data = response.json()
    assert isinstance(sales_data, list)
    assert all(isinstance(item, dict) for item in sales_data)


def test_get_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    assert all(isinstance(category, dict) for category in categories)
