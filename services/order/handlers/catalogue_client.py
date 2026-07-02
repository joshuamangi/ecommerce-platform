# create httpx call
import httpx
from fastapi import status
from utils.config import settings

CATALOGUE_URL = settings.CATALOGUE_URL

# get id and call the Catlogue API
async def get_catalogue(catalogue_id: int, token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CATALOGUE_URL}/catalogue/{catalogue_id}",
            headers={
                "Authorization": token
            }
        )

    print("Status:", response.status_code)
    print("Body:", response.text)

    response.raise_for_status()

    return response.json()