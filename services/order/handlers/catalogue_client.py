# create httpx call
import httpx
from fastapi import status
from utils.config import settings

CATALOGUE_URL = settings.CATALOGUE_URL

# get id and call the Catlogue API
async def get_catalogue(catalogue_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CATALOGUE_URL}/api/catalogue/{catalogue_id}"
        )

        if response.status_code == status.HTTP_404_NOT_FOUND:
            return None
        response.raise_for_status()
        return response.json()