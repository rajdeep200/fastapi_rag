from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=15, le=100)
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    name: str|None = Field(
        default=None,
        min_length=2,
        max_length=50
    )
    email: EmailStr|None = None
    age: int|None = Field(
        default=None,
        ge=15,
        le=100
    )

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
