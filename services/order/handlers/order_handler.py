import datetime

from handlers.catalogue_client import get_catalogue
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.models import Order
from schema.order_schema import OrderBase


class OrderHandler:

    @staticmethod
    async def fetch_all_orders(db: AsyncSession):

        query = select(Order)

        result = await db.execute(query)

        return result.scalars().all()

    @staticmethod
    async def fetch_order_by_id(db: AsyncSession, order_id: int):

        query = select(Order).where(Order.id == order_id)

        result = await db.execute(query)

        return result.scalars().one_or_none()

    @staticmethod
    async def create_order(db: AsyncSession, order: OrderBase):
        # Validate catalogue exists
        catalogue = await get_catalogue(order.catalogue_id)
        if not catalogue:
            return None
        new_order = Order(
            catalogue_id=order.catalogue_id,
            quantity=order.quantity,
            status=order.status
        )
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)
        return new_order
    
    
    @staticmethod
    async def update_order(
        db: AsyncSession,
        order_id: int,
        updated_order: OrderBase
    ):

        query = select(Order).where(Order.id == order_id)

        result = await db.execute(query)

        existing_order = result.scalars().one_or_none()

        if not existing_order:
            return None

        existing_order.catalogue_id = updated_order.catalogue_id
        existing_order.quantity = updated_order.quantity
        existing_order.status = updated_order.status

        await db.commit()

        await db.refresh(existing_order)

        return existing_order

    @staticmethod
    async def delete_order(db: AsyncSession, order_id: int):

        query = select(Order).where(Order.id == order_id)

        result = await db.execute(query)

        existing_order = result.scalars().one_or_none()

        if not existing_order:
            return None

        await db.delete(existing_order)

        await db.commit()

        return existing_order
