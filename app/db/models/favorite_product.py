from sqlalchemy import (
    Column, Integer, DateTime, func, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship

from app.db.database import Base

class FavoriteProduct(Base):
    __tablename__ = "favorite_products"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product")

    __table_args__ = (
        UniqueConstraint("client_id", "product_id", name="uq_client_product"),
    )
