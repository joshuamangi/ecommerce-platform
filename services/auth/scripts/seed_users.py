from sqlalchemy.orm import Session

from data.database import SessionLocal
from data.models import User
from schema.auth_schema import Permissions
from utils.password import PasswordService


USERS = [
    {
        "email": "admin@example.com",
        "password": "Admin123!",
        "permissions": [
            Permissions.CATALOGUE_READ,
            Permissions.CATALOGUE_CREATE,
            Permissions.CATALOGUE_UPDATE,
            Permissions.CATALOGUE_DELETE,
            Permissions.ORDER_READ,
            Permissions.ORDER_CREATE,
        ],
    },
    {
        "email": "catalogue@example.com",
        "password": "Catalogue123!",
        "permissions": [
            Permissions.CATALOGUE_READ,
            Permissions.CATALOGUE_CREATE,
            Permissions.CATALOGUE_UPDATE,
        ],
    },
    {
        "email": "customer@example.com",
        "password": "Customer123!",
        "permissions": [
            Permissions.CATALOGUE_READ,
            Permissions.ORDER_CREATE,
        ],
    },
]


def seed_users():
    db: Session = SessionLocal()

    try:
        for user_data in USERS:
            existing = (
                db.query(User)
                .filter(User.email == user_data["email"])
                .first()
            )

            if existing:
                print(f"Skipping {user_data['email']} (already exists)")
                continue

            user = User(
                email=user_data["email"],
                password_hash=PasswordService.hash_password(
                    user_data["password"]
                ),
                permissions=user_data["permissions"],
                is_active=True,
            )

            db.add(user)

        db.commit()
        print("Users seeded successfully")

    except Exception as ex:
        db.rollback()
        print(f"Failed: {ex}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_users()
