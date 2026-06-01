from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    catalogue_id: int
    quantity: int
    status: str = "pending"


class OrderOut(OrderBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
