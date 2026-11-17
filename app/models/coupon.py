
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Coupon(Base):
    __tablename__ = "coupons"

    __table_args__ = (
        CheckConstraint(
            "length(trim(code)) > 0",
            name="ck_coupons_code_not_empty",
        ),
        CheckConstraint(
            "discount_type IN ('percentage', 'fixed')",
            name="ck_coupons_discount_type_valid",
        ),
        CheckConstraint(
            "discount_value > 0",
            name="ck_coupons_discount_value_positive",
        ),
        CheckConstraint(
            "discount_type != 'percentage' OR discount_value <= 100",
            name="ck_coupons_percentage_max_100",
        ),
        CheckConstraint(
            "minimum_order_amount >= 0",
            name="ck_coupons_minimum_order_nonnegative",
        ),
        CheckConstraint(
            "used_count >= 0",
            name="ck_coupons_used_count_nonnegative",
        ),
        CheckConstraint(
            "usage_limit IS NULL OR usage_limit > 0",
            name="ck_coupons_usage_limit_positive",
        ),
        CheckConstraint(
            "expires_at IS NULL OR starts_at IS NULL OR expires_at > starts_at",
            name="ck_coupons_expiration_after_start",
        ),
        Index(
            "uq_coupons_code_lower",
            text("lower(code)"),
            unique=True,
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    discount_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    discount_value: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    minimum_order_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
        server_default=text("0.00"),
        nullable=False,
    )

    usage_limit: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    used_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        server_default=text("0"),
        nullable=False,
    )

    starts_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="coupon",
        passive_deletes=True,
    )
