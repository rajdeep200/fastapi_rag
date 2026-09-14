from fastapi import FastAPI

from app.routers import users
# from app.database.connection import Base, engine

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI mastery",
    version="1.0.0"
)

app.include_router(users.router)

@app.get("/")
def root():
    return {
        "message": "Server is running"
    }