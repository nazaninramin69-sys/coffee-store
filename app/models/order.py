
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'paid', 'processing', 'shipped', "
            "'delivered', 'cancelled', 'refunded')",
            name="ck_orders_status_valid",
        ),
        CheckConstraint(
            "length(trim(order_number)) > 0",
            name="ck_orders_order_number_not_empty",
        ),
        CheckConstraint(
            "length(trim(shipping_recipient)) > 0",
            name="ck_orders_shipping_recipient_not_empty",
        ),
        CheckConstraint(
            "length(trim(shipping_phone)) > 0",
            name="ck_orders_shipping_phone_not_empty",
        ),
        CheckConstraint(
            "length(trim(shipping_country)) > 0",
            name="ck_orders_shipping_country_not_empty",
        ),
        CheckConstraint(
            "length(trim(shipping_city)) > 0",
            name="ck_orders_shipping_city_not_empty",
        ),
        CheckConstraint(
            "length(trim(shipping_address)) > 0",
            name="ck_orders_shipping_address_not_empty",
        ),
        CheckConstraint(
            "length(trim(shipping_postal_code)) > 0",
            name="ck_orders_shipping_postal_code_not_empty",
        ),
        CheckConstraint(
            "subtotal >= 0",
            name="ck_orders_subtotal_nonnegative",
        ),
        CheckConstraint(
            "discount_amount >= 0",
            name="ck_orders_discount_nonnegative",
        ),
        CheckConstraint(
            "discount_amount <= subtotal",
            name="ck_orders_discount_not_exceed_subtotal",
        ),
        CheckConstraint(
            "shipping_cost >= 0",
            name="ck_orders_shipping_cost_nonnegative",
        ),
        CheckConstraint(
            "total >= 0",
            name="ck_orders_total_nonnegative",
        ),
        CheckConstraint(
            "total = subtotal - discount_amount + shipping_cost",
            name="ck_orders_total_calculation",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    order_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        index=True,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    shipping_recipient: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    shipping_phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    shipping_country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    shipping_city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    shipping_province: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    shipping_address: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    shipping_postal_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    coupon_id: Mapped[int | None] = mapped_column(
        ForeignKey("coupons.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        server_default=text("'pending'"),
        nullable=False,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        server_default=text("0.00"),
        nullable=False,
    )

    shipping_cost: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        server_default=text("0.00"),
        nullable=False,
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="orders",
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        passive_deletes="all",
    )

    coupon: Mapped["Coupon | None"] = relationship(
        back_populates="orders",
    )

    payments: Mapped[list["Payment"]] = relationship(
        back_populates="order",
        passive_deletes="all",
    )
