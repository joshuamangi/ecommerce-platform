# connect to db

from sqlalchemy.orm import Session

from data.models import Catalogue
from schema.catalogue_schema import CatalogueBase


class CatalogueHandler:
    @staticmethod
    def check_catalogue_exists(db: Session, catalogue: CatalogueBase):
        """Checks to see if catalogue already exists"""
        existing_catalogue = db.query(Catalogue).filter(
            Catalogue.sku == catalogue.sku
        ).first()
        return existing_catalogue

    @staticmethod
    def create_catalogue(db: Session, catalogue: CatalogueBase):
        """Creates a new catalogue entry"""
        new_catalogue = Catalogue(
            sku=catalogue.sku,
            name=catalogue.name,
            description=catalogue.description,
        )
        db.add(new_catalogue)
        db.commit()
        db.refresh(new_catalogue)
        return new_catalogue

    @staticmethod
    def fetch_all_catalogues(db: Session):
        return db.query(Catalogue).filter().all()

    @staticmethod
    def fetch_catalogue_by_id(db: Session, sku: str):
        existing_catalogue = db.query(Catalogue).filter(
            Catalogue.sku == sku
        ).first()
        return existing_catalogue
