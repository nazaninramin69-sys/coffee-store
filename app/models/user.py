
from sqlalchemy import Boolean, CheckConstraint, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "length(trim(full_name)) > 0",
            name="ck_users_full_name_not_empty",
        ),
        CheckConstraint(
            "length(trim(email)) > 0",
            name="ck_users_email_not_empty",
        ),
        CheckConstraint(
            "length(trim(hashed_password)) > 0",
            name="ck_users_hashed_password_not_empty",
        ),
        Index(
            "uq_users_email_lower",
            text("lower(email)"),
            unique=True,
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
        nullable=False,
    )

    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text("false"),
        nullable=False,
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="user",
        passive_deletes="all",
    )

    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
