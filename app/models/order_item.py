
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_order_items_quantity_positive",
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="ck_order_items_unit_price_nonnegative",
        ),
        CheckConstraint(
            "total_price >= 0",
            name="ck_order_items_total_price_nonnegative",
        ),
        CheckConstraint(
            "total_price = unit_price * quantity",
            name="ck_order_items_total_price_calculation",
        ),
        CheckConstraint(
            "length(trim(product_name)) > 0",
            name="ck_order_items_product_name_not_empty",
        ),
        CheckConstraint(
            "product_weight_grams > 0",
            name="ck_order_items_product_weight_positive",
        ),
        CheckConstraint(
            "length(trim(product_origin_country)) > 0",
            name="ck_order_items_origin_country_not_empty",
        ),
        CheckConstraint(
            "length(trim(product_processing)) > 0",
            name="ck_order_items_processing_not_empty",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    product_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    product_weight_grams: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    product_origin_country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    product_processing: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    total_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(
        back_populates="items",
    )

    product: Mapped["Product"] = relationship(
        back_populates="order_items",
    )
