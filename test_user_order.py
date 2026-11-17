
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.models.user import User
from app.models.order import Order


def test_user_order_relationship():
    db = SessionLocal()

    email = "user.order.test@example.com"
    order_number = "TEST-ORDER-001"

    try:
        # 1. Create user
        user = User(
            full_name="Order Test User",
            email=email,
            hashed_password="test_hashed_password",
        )

        # 2. Create order
        order = Order(
            order_number=order_number,
            shipping_recipient="Order Test User",
            shipping_phone="09123456789",
            shipping_country="Iran",
            shipping_city="Tehran",
            shipping_address="Test Street, No. 10",
            shipping_postal_code="1234567890",
            subtotal=Decimal("500000.00"),
            discount_amount=Decimal("50000.00"),
            shipping_cost=Decimal("30000.00"),
            total=Decimal("480000.00"),
        )

        # 3. Connect order to user
        user.orders.append(order)

        db.add(user)
        db.commit()

        db.refresh(user)
        db.refresh(order)

        user_id = user.id
        order_id = order.id

        print("User and order created successfully.")

        # 4. Read relationship from User side
        saved_user = db.scalar(
            select(User).where(User.id == user_id)
        )

        print("\nUser -> Orders:")
        for item in saved_user.orders:
            print(f"- {item.order_number}: {item.total}")

        # 5. Read relationship from Order side
        saved_order = db.scalar(
            select(Order).where(Order.id == order_id)
        )

        print("\nOrder -> User:")
        print(f"- {saved_order.user.full_name}")

        # 6. Try deleting user while order exists
        db.delete(saved_user)

        try:
            db.commit()
            print("\nFAILED: User with an existing order was deleted!")

        except IntegrityError:
            db.rollback()
            print("\nPASSED: User with an existing order cannot be deleted.")

        # 7. Verify both records still exist
        remaining_user = db.get(User, user_id)
        remaining_order = db.get(Order, order_id)

        print(f"User still exists: {remaining_user is not None}")
        print(f"Order still exists: {remaining_order is not None}")

        # 8. Clean up test records
        if remaining_order:
            db.delete(remaining_order)
            db.commit()

        if remaining_user:
            db.delete(remaining_user)
            db.commit()

        print("\nTest records deleted successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    test_user_order_relationship()
