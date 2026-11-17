
from decimal import Decimal

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.product import Product


def test_product_crud():
    db = SessionLocal()

    try:
        # 1. Create
        product = Product(
            name="Ethiopia Yirgacheffe",
            slug="ethiopia-yirgacheffe-test",
            description="Specialty coffee with floral and citrus notes.",
            origin_country="Ethiopia",
            origin_region="Yirgacheffe",
            variety="Heirloom",
            altitude=1900,
            processing="Washed",
            tasting_notes="Jasmine, bergamot, lemon",
            weight_grams=250,
            price=Decimal("450000.00"),
            stock=20,
            is_active=True,
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        print("\nProduct created successfully!")
        print(f"ID: {product.id}")
        print(f"Name: {product.name}")
        print(f"Price: {product.price}")

        product_id = product.id

        # 2. Read
        saved_product = db.scalar(
            select(Product).where(Product.id == product_id)
        )

        print("\nProduct retrieved successfully!")
        print(f"Name: {saved_product.name}")
        print(f"Origin: {saved_product.origin_country}")
        print(f"Stock: {saved_product.stock}")

        # 3. Update
        saved_product.stock = 15
        db.commit()
        db.refresh(saved_product)

        print("\nProduct updated successfully!")
        print(f"New stock: {saved_product.stock}")

        # 4. Delete
        db.delete(saved_product)
        db.commit()

        print("\nProduct deleted successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    test_product_crud()
