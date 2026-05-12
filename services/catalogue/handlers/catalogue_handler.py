# connect to db

import orjson
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data.models import Catalogue
from schema.catalogue_schema import CatalogueBase
from data.redis import redis_client


class CatalogueHandler:

    @staticmethod
    async def check_catalogue_exists_by_id(db: AsyncSession, catalogue_id: int):
        """Checks to see if catalogue already exists by id"""
        query = select(Catalogue).where(Catalogue.id == catalogue_id)
        if not query:
            return None
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def check_catalogue_exists_by_sku(db: AsyncSession, catalogue: CatalogueBase):
        """Checks to see if catalogue already exists"""
        query = select(Catalogue).where(Catalogue.sku == catalogue.sku)
        result = await db.execute(query)

        existing_catalogue = result.scalars().first()
        if not existing_catalogue:
            return None
        return existing_catalogue

    @staticmethod
    async def create_catalogue(db: AsyncSession, catalogue: CatalogueBase):
        """Creates a new catalogue entry"""
        new_catalogue = Catalogue(
            sku=catalogue.sku,
            name=catalogue.name,
            description=catalogue.description,
        )
        db.add(new_catalogue)
        await db.commit()
        await db.refresh(new_catalogue)
        return new_catalogue

    @staticmethod
    async def create_deadlock_simulation(sku: str, db: AsyncSession):
        query = (
            select(Catalogue).where(Catalogue.sku == sku).with_for_update()
        )
        result = await db.execute(query)
        item = result.scalars().one()
        item.stock_quantity -= 1
        return item

    @staticmethod
    async def fetch_all_catalogues(db: AsyncSession):
        query = select(Catalogue)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def fetch_catalogue_by_id(db: AsyncSession, id: int):
        key = f"catalogue:{id}:data"

        # Fetch cached data
        try:
            cached_data = await redis_client.get(key)
            if cached_data:
                return orjson.loads(cached_data)
        except Exception as e:
            print(f"Redis error: {e}")

        query = select(Catalogue).where(Catalogue.id == id)
        result = await db.execute(query)
        existing_catalogue = result.scalars().one_or_none()

        if existing_catalogue:
            try:
                data = {
                    "id": existing_catalogue.id,
                    "sku": existing_catalogue.sku,
                    "name": existing_catalogue.name,
                    "description": existing_catalogue.description,
                    "price": existing_catalogue.price,
                    "stock_quantity": existing_catalogue.stock_quantity
                }
                await redis_client.setex(key, 300, orjson.dumps(data))
            except Exception as e:
                print(f"Redis write error: {e}")
        return existing_catalogue

    @staticmethod
    async def update_catalogue(db: AsyncSession, updated_catalogue: CatalogueBase, sku: str):

        query = select(Catalogue).where(Catalogue.sku == sku)
        result = await db.execute(query)
        existing_catalogue = result.scalars().one_or_none()

        if not existing_catalogue:
            return None
        existing_catalogue.price = updated_catalogue.price
        existing_catalogue.description = updated_catalogue.description
        existing_catalogue.stock_quantity = updated_catalogue.stock_quantity
        existing_catalogue.sku = updated_catalogue.sku

        await db.commit()
        await db.refresh(existing_catalogue)
        return existing_catalogue
