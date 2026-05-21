import random
from time import perf_counter
from sqlalchemy import create_engine, insert, text
from data.models import Catalogue

# 1. Define index statements
INDEXES = [
    "CREATE INDEX ix_catalogue_attributes_gin ON catalogue USING gin (attributes);",
    "CREATE INDEX ix_catalogue_tags_gin ON catalogue USING gin (tags);",
    "CREATE INDEX ix_catalogue_price ON catalogue (price);"
]

engine = create_engine("postgresql://user:password@localhost/catalogue")


def seed_data(n=100000):
    # PREPARE: Drop indexes to speed up insertion
    print("Dropping indexes...")
    with engine.begin() as conn:
        conn.execute(text("DROP INDEX IF EXISTS ix_catalogue_attributes_gin;"))
        conn.execute(text("DROP INDEX IF EXISTS ix_catalogue_tags_gin;"))
        conn.execute(text("DROP INDEX IF EXISTS ix_catalogue_price;"))
        conn.execute(
            text("TRUNCATE TABLE catalogue RESTART IDENTITY CASCADE;"))
        conn.execute(text("SET synchronous_commit = OFF;"))

    # GENERATE: Batch data in memory
    print(f"Generating {n} records...")
    products = [
        {
            "sku": f"SKU-{i}",
            "name": f"Product {i}",
            "price": random.uniform(10.0, 1000.0),
            "stock_quantity": random.randint(0, 100),
            "attributes": {"color": random.choice(["red", "blue"]), "power": random.randint(1, 10)}
        } for i in range(n)
    ]

    # INSERT: Do it in one big batch
    print("Inserting data...")
    start_time = perf_counter()
    with engine.begin() as conn:
        conn.execute(insert(Catalogue), products)

    # RECREATE: Indexes are built once on a full table
    print("Recreating indexes...")
    with engine.begin() as conn:
        for idx_sql in INDEXES:
            conn.execute(text(idx_sql))

    print(f"Done in {perf_counter() - start_time:.2f} seconds.")


if __name__ == "__main__":
    seed_data()
