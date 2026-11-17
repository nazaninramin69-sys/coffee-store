
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Address(Base):
    __tablename__ = "addresses"

    __table_args__ = (
        CheckConstraint(
            "length(trim(title)) > 0",
            name="ck_addresses_title_not_empty",
        ),
        CheckConstraint(
            "length(trim(recipient_name)) > 0",
            name="ck_addresses_recipient_name_not_empty",
        ),
        CheckConstraint(
            "length(trim(phone)) > 0",
            name="ck_addresses_phone_not_empty",
        ),
        CheckConstraint(
            "length(trim(country)) > 0",
            name="ck_addresses_country_not_empty",
        ),
        CheckConstraint(
            "length(trim(city)) > 0",
            name="ck_addresses_city_not_empty",
        ),
        CheckConstraint(
            "length(trim(address_line)) > 0",
            name="ck_addresses_address_line_not_empty",
        ),
        CheckConstraint(
            "length(trim(postal_code)) > 0",
            name="ck_addresses_postal_code_not_empty",
        ),
        Index(
            "uq_addresses_one_default_per_user",
            "user_id",
            unique=True,
            postgresql_where=text("is_default = true"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    recipient_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    province: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    address_line: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    postal_code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("false"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="addresses",
    )
