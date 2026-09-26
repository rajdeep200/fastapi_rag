from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from sqlalchemy import select
from app.models.user import User
from app.security import hash_password

def register_user(
    db: Session,
    user_data: UserCreate
):
    existing_user = db.scalar(
        select(User).where(User.email == user_data.email)
    )
    
    def authenticate_user(db: Session, email: str, password: str):
        user = db.scalar(select(User).where(User.email == email))

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def login_user(db: Session, email: str, password: str):
        user = authenticate_user(db, email, password)

        if not user:
            return None

        access_token = create_access_token(data={"sub": str(user.id)})

        return access_token
