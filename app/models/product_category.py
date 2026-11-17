
from sqlalchemy import Column, ForeignKey, Index, Integer, Table

from app.db.base import Base


product_category = Table(
    "product_category",
    Base.metadata,

    Column(
        "product_id",
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        primary_key=True,
    ),

    Column(
        "category_id",
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),

    Index(
        "ix_product_category_category_id",
        "category_id",
    ),
)
