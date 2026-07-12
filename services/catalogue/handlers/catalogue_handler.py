import orjson
import structlog
import asyncio

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from data.models import Catalogue
from data.breaker import database_breaker
from schema.catalogue_schema import CatalogueBase
from data.redis import redis_client

logger = structlog.get_logger(__name__)


class CatalogueHandler:

    @staticmethod
    async def check_catalogue_exists_by_id(db: AsyncSession, catalogue_id: int):
        """Checks to see if catalogue already exists by id"""
        logger.info("Fetching Catalogue", catalogue_id=catalogue_id)
        query = select(Catalogue).where(Catalogue.id == catalogue_id)
        if not query:
            return None
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def check_catalogue_exists_by_sku(db: AsyncSession, catalogue: CatalogueBase):
        """Checks to see if catalogue already exists"""
        logger.info("Fetching Catalogue", catalogue_sku=catalogue.sku)
        query = select(Catalogue).where(Catalogue.sku == catalogue.sku)
        result = await db.execute(query)

        existing_catalogue = result.scalars().first()
        logger.warning("Catalogue not Found")
        if not existing_catalogue:
            return None
        return existing_catalogue

    @staticmethod
    async def create_catalogue(db: AsyncSession, catalogue: CatalogueBase):
        """Creates a new catalogue entry"""
        logger.info("Creating Catalogue", catalogue_name=catalogue.name)
        new_catalogue = Catalogue(
            sku=catalogue.sku,
            name=catalogue.name,
            description=catalogue.description,
        )
        db.add(new_catalogue)
        await db.commit()
        await db.refresh(new_catalogue)
        logger.info("Catalogue Created", catalogue_name=catalogue.name)
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
        logger.info("Fetching catalogue", catalogue_id=id)
        # Fetch cached data
        try:
            cached_data = await redis_client.get(key)
            if cached_data:
                logger.info("Redis cache hit", key=key)
                return orjson.loads(cached_data)
        except Exception as e:
            logger.exception("Redis write failed", key=key)

        query = select(Catalogue).where(Catalogue.id == id)
        async def execute_query():
            await asyncio.sleep(6)
            return await db.execute(query)
        result = await database_breaker.call(execute_query)
        # result = await db.execute(query)
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
                logger.info("Catalogue cached", key=key, ttl=300)
            except Exception as e:
                logger.exception("Redis write failed", key=key)
        return existing_catalogue

    @staticmethod
    async def update_catalogue(db: AsyncSession, updated_catalogue: CatalogueBase, sku: str, id: int):

        key = f"catalogue:{id}:data"
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

        await redis_client.delete(key)
        return existing_catalogue
