
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.models.user import User
from app.models.order import Order
from app.models.payment import Payment


def test_order_payment_relationship():
    db = SessionLocal()

    try:
        user = User(
            full_name="Payment Test User",
            email="payment.test@example.com",
            hashed_password="test_hashed_password",
        )

        order = Order(
            order_number="TEST-PAYMENT-ORDER-001",
            shipping_recipient="Payment Test User",
            shipping_phone="09123456789",
            shipping_country="Iran",
            shipping_city="Tehran",
            shipping_address="Test Street",
            shipping_postal_code="1234567890",
            subtotal=Decimal("500000.00"),
            discount_amount=Decimal("0.00"),
            shipping_cost=Decimal("0.00"),
            total=Decimal("500000.00"),
        )

        payment = Payment(
            amount=Decimal("500000.00"),
            payment_method="online",
            status="successful",
            transaction_id="TEST-TRANSACTION-001",
        )

        user.orders.append(order)
        order.payments.append(payment)

        db.add(user)
        db.commit()

        db.refresh(order)
        db.refresh(payment)

        user_id = user.id
        order_id = order.id
        payment_id = payment.id

        print("User, order and payment created successfully.")

        # Order -> Payments
        saved_order = db.scalar(
            select(Order).where(Order.id == order_id)
        )

        print("\nOrder -> Payments:")
        for saved_payment in saved_order.payments:
            print(
                f"- Amount: {saved_payment.amount} | "
                f"Status: {saved_payment.status}"
            )

        # Payment -> Order
        saved_payment = db.get(Payment, payment_id)

        print("\nPayment -> Order:")
        print(f"- {saved_payment.order.order_number}")

        # Try deleting order while payment exists
        db.delete(saved_order)

        try:
            db.commit()
            print("\nFAILED: Order with existing payment was deleted!")

        except IntegrityError:
            db.rollback()
            print("\nPASSED: Order with existing payment cannot be deleted.")

        print(
            f"Order still exists: "
            f"{db.get(Order, order_id) is not None}"
        )
        print(
            f"Payment still exists: "
            f"{db.get(Payment, payment_id) is not None}"
        )

        # Clean up
        saved_payment = db.get(Payment, payment_id)
        saved_order = db.get(Order, order_id)
        saved_user = db.get(User, user_id)

        db.delete(saved_payment)
        db.commit()

        db.delete(saved_order)
        db.commit()

        db.delete(saved_user)
        db.commit()

        print("\nTest records deleted successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    test_order_payment_relationship()

