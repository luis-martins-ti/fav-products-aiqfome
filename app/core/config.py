from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    database_url: str = Field(..., json_schema_extra={"env": "DATABASE_URL"})
    secret_key: str = Field(..., json_schema_extra={"env": "SECRET_KEY"})
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = ConfigDict(env_file=".env")


settings = Settings()
