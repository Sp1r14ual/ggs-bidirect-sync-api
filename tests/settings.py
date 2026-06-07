from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    TEST_HOUSE_ID: int
    TEST_API_BASE_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file="tests/.env.test", extra="ignore")


test_settings = TestSettings()
