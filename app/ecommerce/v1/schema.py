from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class ProductSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=255)
    description: str = Field(None, min_length=1, max_length=1000)
    price: float = Field(..., ge=0)
    category_id: int


class OrderSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., min_length=1, max_length=255)
    phone: str
    address: str

    product_id: int
    quantity: int
