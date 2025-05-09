from typing import Optional
from pydantic import Field
from app.schemas.base import BaseSchema

class ProductBase(BaseSchema):
    """Base schema for product data."""
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    image: Optional[str] = Field(None, description="Product image URL")

class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    pass

class ProductUpdate(ProductBase):
    """Schema for updating an existing product."""
    name: Optional[str] = Field(None, description="Product name")
    price: Optional[float] = Field(None, gt=0, description="Product price")

class ProductInDB(ProductBase):
    """Schema for product data as stored in database."""
    id: int = Field(..., description="Product ID")

    class Config:
        from_attributes = True

class ProductResponse(ProductInDB):
    """Schema for product response data."""
    pass

class ProductList(BaseSchema):
    """Schema for list of products with pagination."""
    items: list[ProductResponse]
    total: int
    page: int
    size: int 