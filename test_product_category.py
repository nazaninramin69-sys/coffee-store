
from decimal import Decimal

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.category import Category
from app.models.product import Product


def test_product_category_relationship():
    db = SessionLocal()

    try:
        # 1. Create category
        category = Category(
            name="Specialty Coffee",
            slug="specialty-coffee-test",
            description="Test category",
        )

        # 2. Create product
        product = Product(
            name="Ethiopia Yirgacheffe Test",
            slug="ethiopia-yirgacheffe-category-test",
            origin_country="Ethiopia",
            origin_region="Yirgacheffe",
            processing="Washed",
            weight_grams=250,
            price=Decimal("450000.00"),
            stock=10,
        )

        # 3. Connect product and category
        product.categories.append(category)

        db.add(product)
        db.commit()

        db.refresh(product)
        db.refresh(category)

        print("Product and category created successfully.")

        # 4. Read relationship from Product side
        saved_product = db.scalar(
            select(Product).where(Product.id == product.id)
        )

        print("\nProduct -> Categories:")
        for item in saved_product.categories:
            print(f"- {item.name}")

        # 5. Read relationship from Category side
        saved_category = db.scalar(
            select(Category).where(Category.id == category.id)
        )

        print("\nCategory -> Products:")
        for item in saved_category.products:
            print(f"- {item.name}")

        # 6. Remove only the relationship
        saved_product.categories.remove(saved_category)
        db.commit()

        db.refresh(saved_product)
        db.refresh(saved_category)

        print("\nRelationship removed successfully.")

        print(f"Product still exists: {saved_product.id is not None}")
        print(f"Category still exists: {saved_category.id is not None}")

        # 7. Delete test records
        db.delete(saved_product)
        db.delete(saved_category)
        db.commit()

        print("\nTest records deleted successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    test_product_category_relationship()
