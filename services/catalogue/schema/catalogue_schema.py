from typing import Optional
from pydantic import BaseModel


class CatalogueBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int


class CatalogueCreate(CatalogueBase):
    pass


class CatalogueOut(CatalogueBase):
    id: int
