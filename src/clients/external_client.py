from datetime import datetime
from functools import lru_cache

import requests

from core.logger import logger
from core.settings import settings
from domain.models import ExternalNotificationRequest, Trend, TrendNotification


class ExternalClient:
    external_url: str

    def __init__(self):
        self.external_url = settings.external_url

    def send_info_voids(
        self,
        info_voids: list[Trend],
        last_trend_execution: datetime,
        news_path: str = None,
    ):
        notifications = []
        for trend in info_voids:
            single_notification = TrendNotification(
                trend=trend.trend,
                volume=trend.search_volume,
                growth=trend.increase,
                started_at=trend.started_at,
                finished_at=trend.finished_at,
                news_path=news_path,
                keywords=trend.keywords,
                ivs=trend.ivs,
                demand_factor=trend.demand_factor,
                coverage_factor=trend.coverage_factor,
                delay_factor=trend.delay_factor,
                plurality_factor=trend.plurality_factor,
                news_summary=trend.news_summary,
            )
            notifications.append(single_notification)

        payload = ExternalNotificationRequest(
            last_trend_execution=last_trend_execution, infovoids=notifications
        ).model_dump(mode="json")

        response = requests.post(self.external_url, json=payload)
        if not response.ok:
            logger.error(f"External notification failed, error: {response.json()}")


@lru_cache
def get_external_client():
    return ExternalClient()
