import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Catalogue
from utils.config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def simulate_contention(sku: str):
    db = SessionLocal()
    start_time = time.perf_counter()
    try:
        item = db.query(Catalogue).filter(
            Catalogue.sku == sku
        ).with_for_update().one()
        print(f"Lock acquired for {sku}")
        time.sleep(2)

        item.stock_quantity -= 1
        db.commit()
    finally:
        db.close()

    end_time = time.perf_counter()
    print(f"Transaction completed in {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    simulate_contention("A")
