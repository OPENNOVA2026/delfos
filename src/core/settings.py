import sentry_sdk
from pydantic_settings import BaseSettings
from sentry_sdk.integrations.celery import CeleryIntegration


class AzureOpenAISettings(BaseSettings):
    openai_api_version: str = ""
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""


class Settings(BaseSettings):
    name: str = "Delfos"
    description: str = "Service to get InfoVoids"
    environment: str = "local"

    config_id: str = "1"

    openai: AzureOpenAISettings = AzureOpenAISettings()
    debug: bool = False
    celery_broker_url: str = ""

    smtp_host: str = ""
    smtp_port: str = ""
    smtp_sender: str = ""
    smtp_user: str = ""
    smtp_password: str = ""
    email_list: str = ""

    fake_email: bool = False
    aws_access_key: str = ""
    aws_secret_key: str = ""
    aws_region: str = ""
    aws_s3_endpoint: str = ""
    aws_s3_infovoid_bucket: str = "nova-infovoid-news-bucket"

    external_url: str = ""

    sentry_dsn: str = ""
    sentry_tsr: float = 1.0

    serpapi_key: str = ""


settings = Settings()


def init_sentry() -> None:
    if not settings.sentry_dsn:
        return

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        traces_sample_rate=settings.sentry_tsr,
        integrations=[CeleryIntegration()],
    )
