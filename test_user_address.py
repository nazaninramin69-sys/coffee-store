
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.user import User
from app.models.address import Address


def test_user_address_relationship():
    db = SessionLocal()

    try:
        # 1. Create user
        user = User(
            full_name="Test User",
            email="test.user.address@example.com",
            hashed_password="test_hashed_password",
        )

        # 2. Create address
        address = Address(
            title="Home",
            recipient_name="Test User",
            phone="09123456789",
            country="Iran",
            city="Tehran",
            province="Tehran",
            address_line="Test Street, No. 10",
            postal_code="1234567890",
            is_default=True,
        )

        # 3. Connect address to user
        user.addresses.append(address)

        db.add(user)
        db.commit()

        db.refresh(user)
        db.refresh(address)

        user_id = user.id
        address_id = address.id

        print("User and address created successfully.")

        # 4. Read relationship
        saved_user = db.scalar(
            select(User).where(User.id == user_id)
        )

        print("\nUser -> Addresses:")
        for item in saved_user.addresses:
            print(f"- {item.title}: {item.city}")

        # 5. Remove address from user's collection
        saved_user.addresses.remove(saved_user.addresses[0])
        db.commit()

        # 6. Verify address was deleted
        remaining_address = db.get(Address, address_id)

        print("\nAddress removed from user.")
        print(f"Address still exists: {remaining_address is not None}")

        # 7. Verify user still exists
        remaining_user = db.get(User, user_id)

        print(f"User still exists: {remaining_user is not None}")

        # 8. Clean up
        db.delete(remaining_user)
        db.commit()

        print("\nTest user deleted successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    test_user_address_relationship()
