from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_mins: int = 30
    
    class Config:
        env_file = ".env"
        
settings = Settings()