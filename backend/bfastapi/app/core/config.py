from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DesignPilot API"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:zey35@localhost:5432/postgres"

    SECRET_KEY: str = "CHANGE_THIS_SECRET"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


    GROQ_API_KEY:str

    class Config:
        env_file = ".env"

settings = Settings()
