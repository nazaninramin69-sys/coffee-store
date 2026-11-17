
from sqlalchemy import inspect
from sqlalchemy.orm import configure_mappers

import app.models

from app.db.base import Base
from app.db.session import engine


# 1. Configure all ORM relationships
configure_mappers()

print("All models imported successfully!")
print("All relationships configured successfully!")


# 2. Expected database tables
expected_tables = {
    "products",
    "categories",
    "product_category",
    "users",
    "addresses",
    "orders",
    "order_items",
    "coupons",
    "payments",
}

model_tables = set(Base.metadata.tables.keys())

assert model_tables == expected_tables, (
    f"Model tables mismatch!\n"
    f"Missing: {expected_tables - model_tables}\n"
    f"Unexpected: {model_tables - expected_tables}"
)

print("\nAll expected model tables are registered.")


# 3. Inspect actual PostgreSQL tables
inspector = inspect(engine)

database_tables = set(inspector.get_table_names())

missing_tables = expected_tables - database_tables

assert not missing_tables, (
    f"Missing database tables: {missing_tables}"
)

print("All expected tables exist in PostgreSQL.")


# 4. Display tables
print("\nDatabase tables:")

for table_name in sorted(database_tables & expected_tables):
    print("-", table_name)


print("\nPASSED: Final model and database integration test.")
