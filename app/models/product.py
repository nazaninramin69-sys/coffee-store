
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.product_category import product_category


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("price > 0", name="ck_products_price_positive"),
        CheckConstraint("stock >= 0", name="ck_products_stock_nonnegative"),
        CheckConstraint("weight_grams > 0", name="ck_products_weight_positive"),
        CheckConstraint(
            "altitude IS NULL OR altitude > 0",
            name="ck_products_altitude_positive",
        ),
        CheckConstraint(
            "length(trim(name)) > 0",
            name="ck_products_name_not_empty",
        ),
        CheckConstraint(
            "length(trim(slug)) > 0",
            name="ck_products_slug_not_empty",
        ),
        CheckConstraint(
            "length(trim(origin_country)) > 0",
            name="ck_products_origin_country_not_empty",
        ),
        CheckConstraint(
            "length(trim(processing)) > 0",
            name="ck_products_processing_not_empty",
        ),
        Index(
            "uq_products_slug_lower",
            text("lower(slug)"),
            unique=True,
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(180),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    origin_country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    origin_region: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    variety: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    altitude: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    processing: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    tasting_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    weight_grams: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default=text("0"),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
        nullable=False,
    )

    categories: Mapped[list["Category"]] = relationship(
        secondary=product_category,
        back_populates="products",
        passive_deletes=True,
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product",
        passive_deletes="all",
    )
