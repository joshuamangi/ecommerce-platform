# create httpx call
import httpx
import structlog
from fastapi import status
from utils.config import settings

logger = structlog.get_logger(__name__)

CATALOGUE_URL = settings.CATALOGUE_URL

# get id and call the Catlogue API


async def get_catalogue(catalogue_id: int, token: str):
    async with httpx.AsyncClient() as client:
        logger.info("Calling Catalogue service")
        try:
            response = await client.get(
                f"{CATALOGUE_URL}/catalogue/{catalogue_id}",
                headers={
                    "Authorization": token
                }
            )

            logger.info("Catalogue service returned",
                        status=response.status_code)

            response.raise_for_status()

            return response.json()
        except Exception as e:
            logger.error(
                "Catalogue service unavaliable"
            )
