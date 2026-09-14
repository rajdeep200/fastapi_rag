from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services import user_service
from sqlalchemy.orm import Session
from app.dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    return user_service.get_users(db)
    
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return user_service.get_user(db, user_id)
    
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_use(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(user, db)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    return user_service.update_user(db, user_id, user_data)

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return user_service.delete_user(db, user_id)