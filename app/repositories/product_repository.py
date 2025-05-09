import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.products import Products
from app.schemas.product import ProductCreate


class ProductRepository:
    """Repository class for handling Product database operations."""
    
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Products]:
        """Get all products with pagination."""
        return self.db.query(Products).offset(skip).limit(limit).all()

    def get_by_id(self, product_id: str) -> Optional[Products]:
        """Get a product by its ID."""
        return self.db.query(Products).filter(Products.id == product_id).first()

    def create(self, product: ProductCreate) -> Products:
        """Create a new product."""
        db_product = Products()
        db_product.id = uuid.uuid4()  # Generate new UUID
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.image = product.image
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def update(self, product_id: str, product: ProductCreate) -> Optional[Products]:
        """Update an existing product."""
        db_product = self.get_by_id(product_id)
        if db_product:
            for var, value in product.model_dump().items():
                setattr(db_product, var, value)
            self.db.commit()
            self.db.refresh(db_product)
            return db_product
        return None

    def delete(self, product_id: str) -> Optional[Products]:
        """Delete a product."""
        db_product = self.get_by_id(product_id)
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
            return db_product
        return None 