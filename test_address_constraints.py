
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.models.user import User
from app.models.address import Address


def test_default_address_unique():
    db = SessionLocal()

    try:
        user = User(
            full_name="Address Test User",
            email="address.unique.test@example.com",
            hashed_password="test_hashed_password",
        )

        first_address = Address(
            title="Home",
            recipient_name="Address Test User",
            phone="09123456789",
            country="Iran",
            city="Tehran",
            address_line="First Test Street",
            postal_code="1234567890",
            is_default=True,
        )

        second_address = Address(
            title="Office",
            recipient_name="Address Test User",
            phone="09123456789",
            country="Iran",
            city="Tehran",
            address_line="Second Test Street",
            postal_code="1234567890",
            is_default=True,
        )

        user.addresses.extend([first_address, second_address])
        db.add(user)

        try:
            db.commit()
            print("FAILED: Multiple default addresses were accepted!")

        except IntegrityError:
            db.rollback()
            print("PASSED: Multiple default addresses were rejected.")

    finally:
        db.rollback()

        existing_user = db.query(User).filter_by(
            email="address.unique.test@example.com"
        ).first()

        if existing_user:
            db.delete(existing_user)
            db.commit()

        db.close()


if __name__ == "__main__":
    test_default_address_unique()
