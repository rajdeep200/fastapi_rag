from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

def create_user(user_data: UserCreate, db: Session):
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