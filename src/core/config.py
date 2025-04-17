from pydantic import Field, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppBaseSettings(BaseSettings):
    """Базовый класс для настроек приложения с загрузкой из .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )


class RedisSettings(AppBaseSettings):
    """Настройки подключения к Redis."""

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    uri: str | None = None
    host: str = Field(min_length=1)
    port: int = Field(default=6379, ge=1, le=65535)
    max_connections: int = 100

    @computed_field
    def connection_url(self) -> str:
        """URL для подключения к Redis."""
        if self.uri:
            return self.uri
        return f"redis://{self.host}:{self.port}"


class PsqlSettings(AppBaseSettings):
    """Настройки подключения к PostgreSQL."""

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    sync_uri: str | None = None
    uri: str | None = None
    host: str = Field(min_length=1)
    port: int = Field(default=5432, ge=1, le=65535)
    user: str = Field(min_length=1)
    password: str = Field(min_length=1)
    db: str = Field(min_length=1)

    echo: bool = False
    pool_size: int = 20
    max_overflow: int = 10

    @computed_field
    def db_async_uri(self) -> str:
        """URI для асинхронного подключения к PostgreSQL."""
        if self.uri:
            return self.uri
        dsn = MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db,
        )
        return str(dsn)

    @computed_field
    def db_sync_uri(self) -> str:
        """URI для синхронного подключения к PostgreSQL."""
        if self.uri:
            return self.uri
        dsn = MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db,
        )
        return str(dsn)


class Settings(AppBaseSettings):
    """Настройки приложения."""

    analyze_service_url: str = ""

    redis: RedisSettings = Field(default_factory=RedisSettings)
    postgres: PsqlSettings = Field(default_factory=PsqlSettings)


settings = Settings()
