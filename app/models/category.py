
from sqlalchemy import CheckConstraint, Index, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.product_category import product_category


class Category(Base):
    __tablename__ = "categories"

    __table_args__ = (
        CheckConstraint(
            "length(trim(name)) > 0",
            name="ck_categories_name_not_empty",
        ),
        CheckConstraint(
            "length(trim(slug)) > 0",
            name="ck_categories_slug_not_empty",
        ),
        Index(
            "uq_categories_name_lower",
            text("lower(name)"),
            unique=True,
        ),
        Index(
            "uq_categories_slug_lower",
            text("lower(slug)"),
            unique=True,
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    products: Mapped[list["Product"]] = relationship(
        secondary=product_category,
        back_populates="categories",
        passive_deletes=True,
    )
