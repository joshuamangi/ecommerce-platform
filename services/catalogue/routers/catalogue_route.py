import asyncio
import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from data.database import get_db
from handlers.catalogue_handler import CatalogueHandler
from schema.catalogue_schema import CatalogueBase, CatalogueOut
router = APIRouter(prefix="/catalogue", tags=["catalogue"])


# GET
@router.get("/", status_code=status.HTTP_200_OK)
async def get_catalogue(db: AsyncSession = Depends(get_db)):
    # Return dummy catalogue
    existing_catalogues = await CatalogueHandler.fetch_all_catalogues(db=db)
    return existing_catalogues


# GET by catalogue_id
@router.get("/{catalogue_id}", status_code=status.HTTP_200_OK, response_model=CatalogueOut)
async def retrieve_catalogue_by_id(catalogue_id: int, db: AsyncSession = Depends(get_db)):
    """This implements cache aside strategy"""
    existing_catalogue = await CatalogueHandler.fetch_catalogue_by_id(
        db=db, id=catalogue_id)
    if not existing_catalogue:
        raise HTTPException(detail="Catalogue Not Found",
                            status_code=status.HTTP_404_NOT_FOUND)
    return existing_catalogue


# POST
@router.post("/", status_code=status.HTTP_201_CREATED)
async def new_catalogue(catalogue: CatalogueBase, db: AsyncSession = Depends(get_db)):
    existing_catalogue = await CatalogueHandler.check_catalogue_exists_by_sku(
        db=db, catalogue=catalogue)
    if existing_catalogue:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Catalogue already exists")
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
    catalogue_exists = await CatalogueHandler.check_catalogue_exists_by_sku(
        db=db, catalogue=updated_catalogue)
    if not catalogue_exists:
        raise HTTPException(detail="Catalogue Not Found",
                            status_code=status.HTTP_404_NOT_FOUND)
    return await CatalogueHandler.update_catalogue(db=db, sku=updated_catalogue.sku, updated_catalogue=updated_catalogue)
