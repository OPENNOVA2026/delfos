import json
from functools import lru_cache

from pydantic import BaseModel

from src.clients.s3_client import get_s3_client
from src.core.settings import settings


class NewsOrigin(BaseModel):
    name: str
    url: str
    lang: str


class Config(BaseModel):
    description: str
    news_origin: list[NewsOrigin]
    skip_urls: list[str] = []
    trend_filter: list[str] = []


@lru_cache
def get_config(config_id: str | None = None) -> Config:
    selected_config_id = config_id or settings.config_id

    if settings.environment == "local":
        with open("./config.json", encoding="utf-8") as config_file:
            config_content = json.load(config_file)

        config_selected = config_content[selected_config_id]

        if config_selected is None:
            raise FileNotFoundError(
                f"Config with id={selected_config_id} not found in local config.json"
            )

    else:
        s3 = get_s3_client()
        config_selected = s3.get_raw_config_by_id(config_id=selected_config_id)

    return Config.model_validate(config_selected)
