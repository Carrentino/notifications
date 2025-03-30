from functools import lru_cache

from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = Field(default='localhost:9092')
    group_id: str = Field(default='notifications-group')
    topic_notifications_pushes: str = Field(default='notifications_pushes')
    topic_notifications_mails: str = Field(default='notifications_mails')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
        env_prefix='kafka_',
    )

    @property
    def topics(self) -> list[str]:
        return [v for k, v in self.__dict__.items() if k.startswith('topic_')]


class SMTPSettings(BaseSettings):
    server: str = Field(default="smtp.timeweb.ru")
    port: int = 25
    username: str = Field(default="notify@carrentino.ru")
    password: str = Field(default='password')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
        env_prefix='smtp_',
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
    )

    host: str = '0.0.0.0'  # noqa
    port: int = 8080
    workers_count: int = 1
    reload: bool = True

    log_level: str = Field(default='info')
    debug: bool = True
    debug_postgres: bool = False

    environment: str = 'dev'

    postgres_dsn: PostgresDsn = Field(  # type: ignore
        default='postgresql+asyncpg://postgres:postgres@localhost:5432/base'
    )
    test_postgres_dsn: PostgresDsn = Field(  # type: ignore
        default='postgresql+asyncpg://postgres:@localhost:5432/base_test'
    )

    trace_id_header: str = 'X-Trace-Id'
    jwt_key: SecretStr = Field(default=SecretStr('551b8ef09b5e43ddcc45461f854a89b83b9277c6e578f750bf5a6bc3f06d8c08'))
    FIREBASE_CREDENTIALS_PATH: SecretStr = Field(
        default='/Users/oleggrigorev/Documents/carrentino-147b1-0db9fa394048.json'
    )
    kafka: KafkaSettings = KafkaSettings()
    smtp: SMTPSettings = SMTPSettings()
    base_users_url: str = Field(default='https://carrentino.ru/users/api/')


@lru_cache
def get_settings() -> Settings:
    return Settings()
