# create class Product
# create table catalogue
# rows
# id, sku, name, description, price, stock_quantity
from sqlalchemy import Column, DateTime, Float, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB

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
    )
