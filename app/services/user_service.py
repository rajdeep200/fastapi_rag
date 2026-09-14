import logging
from fastapi import HTTPException, status
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

def create_user(user_data: UserCreate, db: Session):
    
    existing_user = db.scalar(
        select(User).where(User.email == user_data.email)
    )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
    
    user = User(
        name = user_data.name,
        email = user_data.email,
        age = user_data.age,
        password = user_data.password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


def get_users(db: Session):
    return db.scalars(
        select(User)
    ).all()
    
def get_user(db:Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return user


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    user = get_user(db, user_id)
    
    update_data = user_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        logger.error(f"Database integrity error on user_id: {user_id} : {e}")
        logger.error(f"DB error => {e.orig}")
        
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
        
    return user


def delete_user(db: Session, user_id: int):
    
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    
    return {
        "message": "user deleted successfully"
    }