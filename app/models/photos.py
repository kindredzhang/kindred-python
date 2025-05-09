from app.models.base import Base
from datetime import datetime
from sqlalchemy import Uuid, Double, Index, PrimaryKeyConstraint, Column, Integer, String, Float, DateTime, Boolean, Text, ARRAY, BigInteger, Identity, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional, List
import uuid

class Photos(Base):
    __tablename__ = 'photos'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='photos_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    url: Mapped[str] = mapped_column(Text)
    title: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(Text)
    tags: Mapped[Optional[list]] = mapped_column(ARRAY(Text()))
    is_featured: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    file_name: Mapped[Optional[str]] = mapped_column(Text)



