
from decimal import Decimal

from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.models.product import Product


def create_product(name, slug):
    return Product(
        name=name,
        slug=slug,
        origin_country="Ethiopia",
        processing="Washed",
        weight_grams=250,
        price=Decimal("450000.00"),
        stock=10,
    )


def test_duplicate_slug():
    db = SessionLocal()

    try:
        first = create_product(
            name="Ethiopia Coffee One",
            slug="ethiopia-yirgacheffe-test",
        )

        db.add(first)
        db.commit()

        print("First product created successfully.")

        second = create_product(
            name="Ethiopia Coffee Two",
            slug="ETHIOPIA-YIRGACHEFFE-TEST",
        )

        db.add(second)
        db.commit()

        print("FAILED: Duplicate slug was accepted!")

    except IntegrityError:
        db.rollback()
        print("PASSED: Case-insensitive duplicate slug was rejected.")

    finally:
        # Remove the first test product if it was created.
        if "first" in locals() and first.id is not None:
            db.delete(first)
            db.commit()

        db.close()


if __name__ == "__main__":
    test_duplicate_slug()
