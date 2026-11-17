
"""Finalize database models.

Revision ID: 2b7d428de38e
Revises: d22d16c74ff2
Create Date: 2026-11-14
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2b7d428de38e"
down_revision: Union[str, Sequence[str], None] = "d22d16c74ff2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Categories: replace case-sensitive uniqueness with case-insensitive indexes.
    op.drop_constraint(
        op.f("categories_name_key"),
        "categories",
        type_="unique",
    )
    op.drop_index(
        op.f("ix_categories_slug"),
        table_name="categories",
    )
    op.create_check_constraint(
        "ck_categories_name_not_empty",
        "categories",
        "length(trim(name)) > 0",
    )
    op.create_check_constraint(
        "ck_categories_slug_not_empty",
        "categories",
        "length(trim(slug)) > 0",
    )
    op.create_index(
        "uq_categories_name_lower",
        "categories",
        [sa.literal_column("lower(name)")],
        unique=True,
    )
    op.create_index(
        "uq_categories_slug_lower",
        "categories",
        [sa.literal_column("lower(slug)")],
        unique=True,
    )

    # Coupons: replace code uniqueness and correct usage_limit semantics.
    op.drop_index(
        op.f("ix_coupons_code"),
        table_name="coupons",
    )
    op.create_index(
        "uq_coupons_code_lower",
        "coupons",
        [sa.literal_column("lower(code)")],
        unique=True,
    )
    op.create_check_constraint(
        "ck_coupons_code_not_empty",
        "coupons",
        "length(trim(code)) > 0",
    )
    op.drop_constraint(
        "ck_coupons_usage_limit_nonnegative",
        "coupons",
        type_="check",
    )
    op.create_check_constraint(
        "ck_coupons_usage_limit_positive",
        "coupons",
        "usage_limit IS NULL OR usage_limit > 0",
    )
    op.create_check_constraint(
        "ck_coupons_expiration_after_start",
        "coupons",
        "expires_at IS NULL OR starts_at IS NULL OR expires_at > starts_at",
    )

    # Order items: immutable product snapshot columns.
    # The existing order_items table was verified empty before this migration.
    op.add_column(
        "order_items",
        sa.Column("product_name", sa.String(length=150), nullable=False),
    )
    op.add_column(
        "order_items",
        sa.Column("product_weight_grams", sa.Integer(), nullable=False),
    )
    op.add_column(
        "order_items",
        sa.Column("product_origin_country", sa.String(length=100), nullable=False),
    )
    op.add_column(
        "order_items",
        sa.Column("product_processing", sa.String(length=100), nullable=False),
    )

    # Order item indexes.
    op.create_index(
        op.f("ix_order_items_order_id"),
        "order_items",
        ["order_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_order_items_product_id"),
        "order_items",
        ["product_id"],
        unique=False,
    )

    # Order item constraints. quantity > 0 and total_price >= 0 already exist.
    op.create_check_constraint(
        "ck_order_items_unit_price_nonnegative",
        "order_items",
        "unit_price >= 0",
    )
    op.create_check_constraint(
        "ck_order_items_total_price_calculation",
        "order_items",
        "total_price = unit_price * quantity",
    )
    op.create_check_constraint(
        "ck_order_items_product_name_not_empty",
        "order_items",
        "length(trim(product_name)) > 0",
    )
    op.create_check_constraint(
        "ck_order_items_product_weight_positive",
        "order_items",
        "product_weight_grams > 0",
    )
    op.create_check_constraint(
        "ck_order_items_origin_country_not_empty",
        "order_items",
        "length(trim(product_origin_country)) > 0",
    )
    op.create_check_constraint(
        "ck_order_items_processing_not_empty",
        "order_items",
        "length(trim(product_processing)) > 0",
    )

    # Order item foreign keys: prevent deleting referenced orders/products.
    op.drop_constraint(
        op.f("order_items_order_id_fkey"),
        "order_items",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("order_items_product_id_fkey"),
        "order_items",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_order_items_product_id_products",
        "order_items",
        "products",
        ["product_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_order_items_order_id_orders",
        "order_items",
        "orders",
        ["order_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # Products: additional validation checks.
    for name, expression in (
        ("ck_products_altitude_positive", "altitude IS NULL OR altitude > 0"),
        ("ck_products_name_not_empty", "length(trim(name)) > 0"),
        ("ck_products_slug_not_empty", "length(trim(slug)) > 0"),
        ("ck_products_origin_country_not_empty", "length(trim(origin_country)) > 0"),
        ("ck_products_processing_not_empty", "length(trim(processing)) > 0"),
    ):
        op.create_check_constraint(name, "products", expression)

    # Products: case-insensitive slug uniqueness.
    op.drop_index(
        op.f("ix_products_slug"),
        table_name="products",
    )
    op.create_index(
        "uq_products_slug_lower",
        "products",
        [sa.literal_column("lower(slug)")],
        unique=True,
    )

    # Users: non-empty values and case-insensitive email uniqueness.
    for name, expression in (
        ("ck_users_full_name_not_empty", "length(trim(full_name)) > 0"),
        ("ck_users_email_not_empty", "length(trim(email)) > 0"),
        ("ck_users_hashed_password_not_empty", "length(trim(hashed_password)) > 0"),
    ):
        op.create_check_constraint(name, "users", expression)

    op.drop_index(
        op.f("ix_users_email"),
        table_name="users",
    )
    op.create_index(
        "uq_users_email_lower",
        "users",
        [sa.literal_column("lower(email)")],
        unique=True,
    )

    # Addresses: non-empty required address fields.
    for name, expression in (
        ("ck_addresses_title_not_empty", "length(trim(title)) > 0"),
        ("ck_addresses_recipient_name_not_empty", "length(trim(recipient_name)) > 0"),
        ("ck_addresses_phone_not_empty", "length(trim(phone)) > 0"),
        ("ck_addresses_country_not_empty", "length(trim(country)) > 0"),
        ("ck_addresses_city_not_empty", "length(trim(city)) > 0"),
        ("ck_addresses_address_line_not_empty", "length(trim(address_line)) > 0"),
        ("ck_addresses_postal_code_not_empty", "length(trim(postal_code)) > 0"),
    ):
        op.create_check_constraint(name, "addresses", expression)

    # Orders: discount column and validation.
    op.add_column(
        "orders",
        sa.Column(
            "discount_amount",
            sa.Numeric(precision=12, scale=2),
            server_default=sa.text("0.00"),
            nullable=False,
        ),
    )
    for name, expression in (
        ("ck_orders_order_number_not_empty", "length(trim(order_number)) > 0"),
        ("ck_orders_shipping_recipient_not_empty", "length(trim(shipping_recipient)) > 0"),
        ("ck_orders_shipping_phone_not_empty", "length(trim(shipping_phone)) > 0"),
        ("ck_orders_shipping_country_not_empty", "length(trim(shipping_country)) > 0"),
        ("ck_orders_shipping_city_not_empty", "length(trim(shipping_city)) > 0"),
        ("ck_orders_shipping_address_not_empty", "length(trim(shipping_address)) > 0"),
        ("ck_orders_shipping_postal_code_not_empty", "length(trim(shipping_postal_code)) > 0"),
        ("ck_orders_discount_nonnegative", "discount_amount >= 0"),
        ("ck_orders_discount_not_exceed_subtotal", "discount_amount <= subtotal"),
        ("ck_orders_total_calculation", "total = subtotal - discount_amount + shipping_cost"),
    ):
        op.create_check_constraint(name, "orders", expression)

    op.create_index(
        op.f("ix_orders_coupon_id"),
        "orders",
        ["coupon_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_orders_user_id"),
        "orders",
        ["user_id"],
        unique=False,
    )

    # Payments: updated_at, expanded status values, and validation.
    op.add_column(
        "payments",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.drop_constraint(
        "ck_payments_status_valid",
        "payments",
        type_="check",
    )
    op.create_check_constraint(
        "ck_payments_status_valid",
        "payments",
        "status IN ('pending', 'successful', 'failed', 'refunded')",
    )
    op.create_check_constraint(
        "ck_payments_method_not_empty",
        "payments",
        "length(trim(payment_method)) > 0",
    )
    op.create_check_constraint(
        "ck_payments_transaction_id_not_empty",
        "payments",
        "transaction_id IS NULL OR length(trim(transaction_id)) > 0",
    )

    op.drop_constraint(
        op.f("payments_order_id_fkey"),
        "payments",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_payments_order_id_orders",
        "payments",
        "orders",
        ["order_id"],
        ["id"],
        ondelete="RESTRICT",
    )

    # Product-category association index.
    op.create_index(
        "ix_product_category_category_id",
        "product_category",
        ["category_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Product-category association index.
    op.drop_index(
        "ix_product_category_category_id",
        table_name="product_category",
    )

    # Payments.
    op.drop_constraint(
        "fk_payments_order_id_orders",
        "payments",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("payments_order_id_fkey"),
        "payments",
        "orders",
        ["order_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(
        "ck_payments_transaction_id_not_empty",
        "payments",
        type_="check",
    )
    op.drop_constraint(
        "ck_payments_method_not_empty",
        "payments",
        type_="check",
    )
    op.drop_constraint(
        "ck_payments_status_valid",
        "payments",
        type_="check",
    )
    op.create_check_constraint(
        "ck_payments_status_valid",
        "payments",
        "status IN ('pending', 'successful', 'failed')",
    )
    op.drop_column("payments", "updated_at")

    # Orders.
    op.drop_index(
        op.f("ix_orders_user_id"),
        table_name="orders",
    )
    op.drop_index(
        op.f("ix_orders_coupon_id"),
        table_name="orders",
    )
    for name in (
        "ck_orders_total_calculation",
        "ck_orders_discount_not_exceed_subtotal",
        "ck_orders_discount_nonnegative",
        "ck_orders_shipping_postal_code_not_empty",
        "ck_orders_shipping_address_not_empty",
        "ck_orders_shipping_city_not_empty",
        "ck_orders_shipping_country_not_empty",
        "ck_orders_shipping_phone_not_empty",
        "ck_orders_shipping_recipient_not_empty",
        "ck_orders_order_number_not_empty",
    ):
        op.drop_constraint(name, "orders", type_="check")
    op.drop_column("orders", "discount_amount")

    # Addresses.
    for name in (
        "ck_addresses_postal_code_not_empty",
        "ck_addresses_address_line_not_empty",
        "ck_addresses_city_not_empty",
        "ck_addresses_country_not_empty",
        "ck_addresses_phone_not_empty",
        "ck_addresses_recipient_name_not_empty",
        "ck_addresses_title_not_empty",
    ):
        op.drop_constraint(name, "addresses", type_="check")

    # Users.
    op.drop_index(
        "uq_users_email_lower",
        table_name="users",
    )
    op.create_index(
        op.f("ix_users_email"),
        "users",
        ["email"],
        unique=True,
    )
    for name in (
        "ck_users_hashed_password_not_empty",
        "ck_users_email_not_empty",
        "ck_users_full_name_not_empty",
    ):
        op.drop_constraint(name, "users", type_="check")

    # Products.
    op.drop_index(
        "uq_products_slug_lower",
        table_name="products",
    )
    op.create_index(
        op.f("ix_products_slug"),
        "products",
        ["slug"],
        unique=True,
    )
    for name in (
        "ck_products_processing_not_empty",
        "ck_products_origin_country_not_empty",
        "ck_products_slug_not_empty",
        "ck_products_name_not_empty",
        "ck_products_altitude_positive",
    ):
        op.drop_constraint(name, "products", type_="check")

    # Order items.
    op.drop_constraint(
        "fk_order_items_product_id_products",
        "order_items",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_order_items_order_id_orders",
        "order_items",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("order_items_product_id_fkey"),
        "order_items",
        "products",
        ["product_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("order_items_order_id_fkey"),
        "order_items",
        "orders",
        ["order_id"],
        ["id"],
        ondelete="CASCADE",
    )
    for name in (
        "ck_order_items_processing_not_empty",
        "ck_order_items_origin_country_not_empty",
        "ck_order_items_product_weight_positive",
        "ck_order_items_product_name_not_empty",
        "ck_order_items_total_price_calculation",
        "ck_order_items_unit_price_nonnegative",
    ):
        op.drop_constraint(name, "order_items", type_="check")
    op.drop_index(
        op.f("ix_order_items_product_id"),
        table_name="order_items",
    )
    op.drop_index(
        op.f("ix_order_items_order_id"),
        table_name="order_items",
    )
    op.drop_column("order_items", "product_processing")
    op.drop_column("order_items", "product_origin_country")
    op.drop_column("order_items", "product_weight_grams")
    op.drop_column("order_items", "product_name")

    # Coupons.
    op.drop_constraint(
        "ck_coupons_expiration_after_start",
        "coupons",
        type_="check",
    )
    op.drop_constraint(
        "ck_coupons_usage_limit_positive",
        "coupons",
        type_="check",
    )
    op.create_check_constraint(
        "ck_coupons_usage_limit_nonnegative",
        "coupons",
        "usage_limit IS NULL OR usage_limit >= 0",
    )
    op.drop_constraint(
        "ck_coupons_code_not_empty",
        "coupons",
        type_="check",
    )
    op.drop_index(
        "uq_coupons_code_lower",
        table_name="coupons",
    )
    op.create_index(
        op.f("ix_coupons_code"),
        "coupons",
        ["code"],
        unique=True,
    )

    # Categories.
    op.drop_index(
        "uq_categories_slug_lower",
        table_name="categories",
    )
    op.drop_index(
        "uq_categories_name_lower",
        table_name="categories",
    )
    op.drop_constraint(
        "ck_categories_slug_not_empty",
        "categories",
        type_="check",
    )
    op.drop_constraint(
        "ck_categories_name_not_empty",
        "categories",
        type_="check",
    )
    op.create_index(
        op.f("ix_categories_slug"),
        "categories",
        ["slug"],
        unique=True,
    )
    op.create_unique_constraint(
        op.f("categories_name_key"),
        "categories",
        ["name"],
        postgresql_nulls_not_distinct=False,
    )
