import random

from time import perf_counter

from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy import text

from data.models import Catalogue
from data.models import Inventory


INDEXES = [

    "CREATE INDEX ix_catalogue_attributes_gin ON catalogue USING gin (attributes);",

    "CREATE INDEX ix_catalogue_tags_gin ON catalogue USING gin (tags);",

    "CREATE INDEX ix_catalogue_price ON catalogue (price);",

    "CREATE INDEX ix_catalogue_is_active ON catalogue (is_active);",

    "CREATE INDEX ix_catalogue_category_price ON catalogue (category, price);"
]


engine = create_engine(
    "postgresql://user:password@localhost/catalogue"
)


def seed_data(n=100000):

    print("Dropping indexes...")

    with engine.begin() as conn:

        conn.execute(text("""
            DROP INDEX IF EXISTS ix_catalogue_attributes_gin;
        """))

        conn.execute(text("""
            DROP INDEX IF EXISTS ix_catalogue_tags_gin;
        """))

        conn.execute(text("""
            DROP INDEX IF EXISTS ix_catalogue_price;
        """))

        conn.execute(text("""
            DROP INDEX IF EXISTS ix_catalogue_is_active;
        """))

        conn.execute(text("""
            DROP INDEX IF EXISTS ix_catalogue_category_price;
        """))

        conn.execute(text("""
            TRUNCATE TABLE inventory RESTART IDENTITY CASCADE;
        """))

        conn.execute(text("""
            TRUNCATE TABLE catalogue RESTART IDENTITY CASCADE;
        """))

        conn.execute(text("""
            SET synchronous_commit = OFF;
        """))

    print(f"Generating {n} records...")

    catalogues = []

    inventories = []

    categories = [
        "electronics",
        "books",
        "fashion",
        "gaming",
        "fitness"
    ]

    for i in range(n):

        catalogues.append({
            "id": i + 1,
            "sku": f"SKU-{i}",
            "name": f"Product {i}",
            "description": f"Description {i}",
            "price": random.uniform(10.0, 1000.0),
            "attributes": {
                "color": random.choice(["red", "blue"]),
                "power": random.randint(1, 10)
            },
            "tags": [
                random.choice(["popular", "new", "sale"])
            ],
            "is_active": random.choice([True, False]),
            "category": random.choice(categories)
        })

        inventories.append({
            "catalogue_id": i + 1,
            "stock_quantity": random.randint(0, 100),
            "warehouse_location": random.choice(
                ["A1", "B1", "C1"]
            )
        })

    print("Inserting data...")

    start = perf_counter()

    with engine.begin() as conn:

        conn.execute(
            insert(Catalogue),
            catalogues
        )

        conn.execute(
            insert(Inventory),
            inventories
        )

    print("Recreating indexes...")

    with engine.begin() as conn:

        for idx_sql in INDEXES:
            conn.execute(text(idx_sql))

    print(
        f"Done in {perf_counter() - start:.2f} seconds."
    )


if __name__ == "__main__":
    seed_data()
