from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped

from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )
    
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    
    
    