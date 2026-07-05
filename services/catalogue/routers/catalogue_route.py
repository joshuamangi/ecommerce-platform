import asyncio
import socket
import structlog

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from data.database import get_db
from handlers.catalogue_handler import CatalogueHandler
from schema.catalogue_schema import CatalogueBase, CatalogueOut
from services.common.security.auth import get_current_user
from services.common.security.permission import require_permission

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/catalogue", tags=["catalogue"])


@router.get("/health", status_code=status.HTTP_200_OK)
def get_health():
    logger.info("Retrieving heartbeat health")
    return {
        "status": "Successful"
    }


@router.get("/hostname")
def hostname():
    logger.info("Retrieving Hostname")

    return {
        "hostname": socket.gethostname()
    }
# GET


@router.get("/", status_code=status.HTTP_200_OK)
async def get_catalogue(permission=Depends(require_permission(permission='catalogue:read')), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    # Return dummy catalogue
    logger.info("Retrieving all catalogues", user=user["sub"])

    existing_catalogues = await CatalogueHandler.fetch_all_catalogues(db=db)

    logger.info("Retrieved all catalogues")
    return existing_catalogues

# GET by catalogue_id


@router.get("/{catalogue_id}", status_code=status.HTTP_200_OK, response_model=CatalogueOut)
async def retrieve_catalogue_by_id(catalogue_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    """This implements cache aside strategy"""
    logger.info("Retrieving catalogue",
                catalogue_id=catalogue_id, user=user["sub"])
    existing_catalogue = await CatalogueHandler.fetch_catalogue_by_id(
        db=db, id=catalogue_id)
    if not existing_catalogue:
        logger.warning("Catalogue Not Found", catalogue_id=catalogue_id)
        raise HTTPException(detail="Catalogue Not Found",
                            status_code=status.HTTP_404_NOT_FOUND)
    logger.info("Catalogue returned", catalogue_id=catalogue_id)
    return existing_catalogue


# POST
@router.post("/", status_code=status.HTTP_201_CREATED)
async def new_catalogue(catalogue: CatalogueBase, db: AsyncSession = Depends(get_db)):
    logger.info("Creating Catalogue", catalogue_name=catalogue.name)
    existing_catalogue = await CatalogueHandler.check_catalogue_exists_by_sku(
        db=db, catalogue=catalogue)
    if existing_catalogue:
        logger.warning("Catalogue exists", catalogue_name=catalogue.name)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Catalogue already exists")
    logger.info("Catalogue returned", catalogue_name=catalogue.name)
    return await CatalogueHandler.create_catalogue(
        db=db, catalogue=catalogue)

# POST


@router.post("/simulate-deadlock")
async def simulate_deadlock(sku1: str, sku2: str, reverse: bool = False, db: AsyncSession = Depends(get_db)):
    first_sku, second_sku = (sku2, sku1) if reverse else (sku1, sku2)
    item1 = await CatalogueHandler.create_deadlock_simulation(
        sku=first_sku, db=db)

    await asyncio.sleep(4)

    item2 = await CatalogueHandler.create_deadlock_simulation(
        sku=second_sku, db=db)

    await db.commit()

    return {"message": "success"}

# PUT


@router.put("/{catalogue_id}", status_code=status.HTTP_201_CREATED)
async def edit_catalogue(catalogue_id: int, updated_catalogue: CatalogueBase, db: AsyncSession = Depends(get_db)):
    logger.info("Editing Catalogue", catalogue_id=catalogue_id)
    catalogue_exists = await CatalogueHandler.check_catalogue_exists_by_sku(
        db=db, catalogue=updated_catalogue)
    if not catalogue_exists:
        logger.warning("Catalogue Not Found", catalogue_id=catalogue_id)
        raise HTTPException(detail="Catalogue Not Found",
                            status_code=status.HTTP_404_NOT_FOUND)
    logger.info("Catalogue Edited", catalogue_id=catalogue_id)
    return await CatalogueHandler.update_catalogue(db=db, id=catalogue_id, sku=updated_catalogue.sku, updated_catalogue=updated_catalogue)
