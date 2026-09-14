from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20)
    email: str
    age: int = Field(ge=15, le=100)
    password: str = Field(min_length=8)
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    