from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    RUN_MODE: str
    DB_ENGINE_STRING: str
    BITRIX_WEBHOOK: str

    OBJECT_KS_ENTITY_ID: str
    OBJECT_KS_TYPE_ID: int

    GASIFICATION_STAGE_ENTITY_ID: str
    GASIFICATION_STAGE_TYPE_ID: int

    CONTACT_ENTITY_ID: str
    COMPANY_ENTITY_ID: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()