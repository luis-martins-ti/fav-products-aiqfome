from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, func
)

from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    image = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    rating_rate = Column(Float, nullable=True)
    rating_count = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())