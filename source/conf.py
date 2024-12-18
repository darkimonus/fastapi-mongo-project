from pathlib import Path
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
)
from pydantic.fields import FieldInfo
from typing import Optional, List, Any, Type, Tuple
import json

# if environ.get('TESTING') == 'TRUE':
#     database_name = f'test-{MONGO_DB_NAME}'


class MyCustomSource(EnvSettingsSource):
    def prepare_field_value(
            self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        if field_name == 'allowed_hosts':
            return [str(x) for x in value.split(', ')]
        print(value)
        return json.loads(value)


class DatabaseSettings(BaseSettings):
    mongo_host: str
    mongo_port: str
    mongo_user: str
    mongo_pass: str
    mongo_db_name: str


class AuthJWT(BaseSettings):
    access_private_key_path: Path
    access_public_key_path: Path
    refresh_private_key_path: Path
    refresh_public_key_path: Path
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    sms_verification: bool


class RedisSettings(BaseSettings):
    redis_port: str = '6379'
    redis_host: str
    redis_password: Optional[str] = None


class SMSSettings(BaseSettings):
    sms_verification: bool
    default_country_code: str


class TwilioSettings(BaseSettings):
    twilio_sid: str
    twilio_auth_token: str
    twilio_sender_phone: str


class CelerySettings(BaseSettings):
    celery_name: str


class CorsSettings(BaseSettings):
    allowed_hosts: List[str]

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (MyCustomSource(settings_cls),)


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DatabaseSettings = DatabaseSettings()
    auth_jwt: AuthJWT = AuthJWT()

    redis: RedisSettings = RedisSettings()
    deployment_server: bool
    reservation_before_and_after_time: int
    sms: SMSSettings = SMSSettings()
    twilio: TwilioSettings = TwilioSettings()
    celery: CelerySettings = CelerySettings()
    cors_settings: CorsSettings = CorsSettings()


settings = Settings(_case_sensitive=False, _env_file='prod.env', _env_file_encoding='utf-8')
