from app.models.base import Base
from datetime import datetime
from sqlalchemy import Double, Index, PrimaryKeyConstraint, Column, Integer, String, Float, DateTime, Boolean, Text, ARRAY, BigInteger, Identity, text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional, List

class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='products_pkey'),
        Index('ix_products_id', 'id'),
        Index('ix_products_name', 'name')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String)
    price: Mapped[Optional[float]] = mapped_column(Double(53))
    image: Mapped[Optional[str]] = mapped_column(String)
