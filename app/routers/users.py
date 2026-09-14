from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service
from sqlalchemy.orm import Session
from app.dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
def get_users():
    return [
        {
            "id": 1,
            "name": "Rajdeep",
            "email": "rajdeep@example.com",
            "age": 25
        }
    ]
    
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return {
        "id": 1,
        "name": "Rajdeep",
        "email": "rajdeep@example.com",
        "age": 25
    }
    
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_use(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(user, db)

# @router.get("/profile")
# def get_user_profile(
#     current_user: dict = Depends(get_current_user)
# ):
#     return {
#         "message": "Profile fetched successfully",
#         "user": current_user
#     }