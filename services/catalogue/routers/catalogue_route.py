from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from data.database import get_db
from handlers.catalogue_handler import CatalogueHandler
from schema.catalogue_schema import CatalogueBase
import time
router = APIRouter(prefix="/catalogue", tags=["catalogue"])


# GET
@router.get("/")
def get_catalogue(db: Session = Depends(get_db)):
    # Return dummy catalogue
    existing_catalogues = CatalogueHandler.fetch_all_catalogues(db=db)
    return existing_catalogues


# POST
@router.post("/", status_code=status.HTTP_201_CREATED)
def new_catalogue(catalogue: CatalogueBase, db: Session = Depends(get_db)):
    existing_catalogue = CatalogueHandler.check_catalogue_exists(
        db=db, catalogue=catalogue)
    if (existing_catalogue):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Catalogue already exists")
    return CatalogueHandler.create_catalogue(
        db=db, catalogue=catalogue)

# POST


@router.post("/simulate-deadlock")
def simulate_deadlock(sku1: str, sku2: str, reverse: bool = False, db: Session = Depends(get_db)):
    first_sku, second_sku = (sku2, sku1) if reverse else (sku1, sku2)
    item1 = CatalogueHandler.create_deadlock_simulation(
        sku=first_sku, db=db)

    time.sleep(4)

    item2 = CatalogueHandler.create_deadlock_simulation(
        sku=second_sku, db=db)

    db.commit()

    return {"message": "success"}

# PUT


@router.put("/{catalogue_id}", status_code=status.HTTP_201_CREATED)
def edit_catalogue(catalogue_id: int, updated_catalogue: CatalogueBase, db: Session = Depends(get_db)):
    catalogue_exists = CatalogueHandler.check_catalogue_exists(
        db=db, catalogue=updated_catalogue)
    if not catalogue_exists:
        raise HTTPException(detail="Catalogue Not Found",
                            status_code=status.HTTP_404_NOT_FOUND)
    return CatalogueHandler.update_catalogue(db=db, sku=updated_catalogue.sku, updated_catalogue=updated_catalogue)
