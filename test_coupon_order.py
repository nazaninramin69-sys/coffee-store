
from decimal import Decimal

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.user import User
from app.models.order import Order
from app.models.coupon import Coupon


def test_coupon_order_relationship():
    db = SessionLocal()

    try:
        user = User(
            full_name="Coupon Test User",
            email="coupon.test@example.com",
            hashed_password="test_hashed_password",
        )

        coupon = Coupon(
            code="TESTCOUPON",
            discount_type="percentage",
            discount_value=Decimal("10.00"),
            minimum_order_amount=Decimal("100000.00"),
            usage_limit=100,
        )

        order = Order(
            order_number="TEST-COUPON-ORDER-001",
            shipping_recipient="Coupon Test User",
            shipping_phone="09123456789",
            shipping_country="Iran",
            shipping_city="Tehran",
            shipping_address="Test Street",
            shipping_postal_code="1234567890",
            subtotal=Decimal("500000.00"),
            discount_amount=Decimal("50000.00"),
            shipping_cost=Decimal("0.00"),
            total=Decimal("450000.00"),
        )

        user.orders.append(order)
        order.coupon = coupon

        db.add(user)
        db.commit()

        db.refresh(order)
        db.refresh(coupon)

        user_id = user.id
        coupon_id = coupon.id
        order_id = order.id

        print("User, coupon and order created successfully.")

        # Order -> Coupon
        saved_order = db.scalar(
            select(Order).where(Order.id == order_id)
        )

        print("\nOrder -> Coupon:")
        print(f"- Code: {saved_order.coupon.code}")
        print(f"- Discount: {saved_order.discount_amount}")

        # Coupon -> Orders
        saved_coupon = db.get(Coupon, coupon_id)

        print("\nCoupon -> Orders:")
        for coupon_order in saved_coupon.orders:
            print(f"- {coupon_order.order_number}")

        # Delete coupon
        db.delete(saved_coupon)
        db.commit()

        # Verify SET NULL
        db.expire_all()

        saved_order = db.get(Order, order_id)

        print("\nAfter coupon deletion:")
        print(f"Order still exists: {saved_order is not None}")
        print(f"Order coupon_id: {saved_order.coupon_id}")
        print(f"Order coupon relationship: {saved_order.coupon}")
        print(f"Discount amount preserved: {saved_order.discount_amount}")

        # Clean up
        db.delete(saved_order)
        db.commit()

        saved_user = db.get(User, user_id)
        db.delete(saved_user)
        db.commit()

        print("\nTest records deleted successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    test_coupon_order_relationship()

