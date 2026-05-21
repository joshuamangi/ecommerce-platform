# create class Product
# create table catalogue
# rows
# id, sku, name, description, price, stock_quantity
from sqlalchemy import CheckConstraint, Column, DateTime, Float, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from data.database import Base


class Catalogue(Base):
    __tablename__ = "catalogue"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False, default=0.0, index=True)
    stock_quantity = Column(Integer, nullable=False, default=0)
    attributes = Column(JSONB, nullable=True, default=dict)
    tags = Column(ARRAY(String), nullable=False, default=list)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False,
                        server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index(
            "ix_catalogue_attributes_gin",
            "attributes",
            postgresql_using="gin"
        ),
        Index(
            "ix_catalogue_tags_gin",
            "tags",
            postgresql_using="gin"
        )
    )


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    catalogue_id = Column(Integer, ForeignKey("catalogue.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, default="pending")

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )
