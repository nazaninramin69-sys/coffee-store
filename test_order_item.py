
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem


def test_order_item_relationship():
    db = SessionLocal()

    try:
        # 1. Create user
        user = User(
            full_name="Order Item Test User",
            email="order.item.test@example.com",
            hashed_password="test_hashed_password",
        )

        # 2. Create product
        product = Product(
            name="Ethiopia Test Coffee",
            slug="ethiopia-order-item-test",
            origin_country="Ethiopia",
            processing="Washed",
            weight_grams=250,
            price=Decimal("450000.00"),
            stock=10,
        )

        # 3. Create order
        order = Order(
            order_number="TEST-ITEM-ORDER-001",
            shipping_recipient="Order Item Test User",
            shipping_phone="09123456789",
            shipping_country="Iran",
            shipping_city="Tehran",
            shipping_address="Test Street",
            shipping_postal_code="1234567890",
            subtotal=Decimal("900000.00"),
            discount_amount=Decimal("0.00"),
            shipping_cost=Decimal("0.00"),
            total=Decimal("900000.00"),
        )

        # 4. Create order item
        item = OrderItem(
            product_name="Ethiopia Test Coffee",
            product_weight_grams=250,
            product_origin_country="Ethiopia",
            product_processing="Washed",
            quantity=2,
            unit_price=Decimal("450000.00"),
            total_price=Decimal("900000.00"),
        )

        # 5. Connect relationships
        user.orders.append(order)
        order.items.append(item)
        item.product = product

        db.add(user)
        db.commit()

        db.refresh(order)
        db.refresh(item)

        user_id = user.id
        product_id = product.id
        order_id = order.id
        item_id = item.id

        print("User, product, order and order item created successfully.")

        # 6. Read Order -> OrderItems
        saved_order = db.scalar(
            select(Order).where(Order.id == order_id)
        )

        print("\nOrder -> Items:")
        for order_item in saved_order.items:
            print(
                f"- {order_item.product_name} | "
                f"Quantity: {order_item.quantity} | "
                f"Total: {order_item.total_price}"
            )

        # 7. Read OrderItem -> Product
        saved_item = db.scalar(
            select(OrderItem).where(OrderItem.id == item_id)
        )

        print("\nOrderItem -> Product:")
        print(f"- {saved_item.product.name}")

        # 8. Try deleting order while item exists
        db.delete(saved_order)

        try:
            db.commit()
            print("\nFAILED: Order with existing items was deleted!")

        except IntegrityError:
            db.rollback()
            print("\nPASSED: Order with existing items cannot be deleted.")

        # 9. Verify records still exist
        print(f"Order still exists: {db.get(Order, order_id) is not None}")
        print(f"OrderItem still exists: {db.get(OrderItem, item_id) is not None}")

        # 10. Clean up in correct order
        saved_item = db.get(OrderItem, item_id)
        saved_order = db.get(Order, order_id)
        saved_product = db.get(Product, product_id)
        saved_user = db.get(User, user_id)

        db.delete(saved_item)
        db.commit()

        db.delete(saved_order)
        db.commit()

        db.delete(saved_product)
        db.delete(saved_user)
        db.commit()

        print("\nTest records deleted successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    test_order_item_relationship()
