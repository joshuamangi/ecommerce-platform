# create class Product
# create table catalogue
# rows
# id, sku, name, description, price, stock_quantity
from sqlalchemy import Column, Float, Integer, String, Text

from data.database import Base


class Catalogue(Base):
    __tablename__ = "catalogue"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False, default=0.0)
    stock_quantity = Column(Integer, nullable=False, default=0)
