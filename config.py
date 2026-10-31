from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_NAME: str
    DB_PASSWORD: str

    redis_host: str 
    redis_port: int 

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def DATEBASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
