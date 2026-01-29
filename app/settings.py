from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    RUN_MODE: str
    DB_ENGINE_STRING: str
    BITRIX_WEBHOOK: str 
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()