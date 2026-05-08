from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from data.database import get_db
from handlers.catalogue_handler import CatalogueHandler
from schema.catalogue_schema import CatalogueBase
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
