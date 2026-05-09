# connect to db

from sqlalchemy.orm import Session
from data.models import Catalogue
from schema.catalogue_schema import CatalogueBase
import time


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
    def create_deadlock_simulation(sku: str, db: Session):
        item = db.query(Catalogue).filter(
            Catalogue.sku == sku).with_for_update().one()
        item.stock_quantity -= 1
        return

    @staticmethod
    def fetch_all_catalogues(db: Session):
        return db.query(Catalogue).filter().all()

    @staticmethod
    def fetch_catalogue_by_id(db: Session, sku: str):
        existing_catalogue = db.query(Catalogue).filter(
            Catalogue.sku == sku
        ).first()
        return existing_catalogue

    @staticmethod
    def update_catalogue(db: Session, updated_catalogue: CatalogueBase, sku: str):

        existing_catalogue = db.query(Catalogue).filter(
            Catalogue.sku == sku
        ).with_for_update().one_or_none()

        if not existing_catalogue:
            return None
        existing_catalogue.price = updated_catalogue.price
        existing_catalogue.description = updated_catalogue.description
        existing_catalogue.stock_quantity = updated_catalogue.stock_quantity
        existing_catalogue.sku = updated_catalogue.sku

        db.commit()
        db.refresh(existing_catalogue)
        return existing_catalogue
