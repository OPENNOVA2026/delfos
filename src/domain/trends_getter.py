from datetime import datetime, timezone

from serpapi import GoogleSearch

from core.settings import settings
from domain.models import Trend
from src.core.config import get_config


class SearchTrends:
    def __init__(self):
        self.params = {
            "api_key": settings.serpapi_key,
            "engine": "google_trends_trending_now",
            "geo": "ES",
            "hl": "es",
            "only_active": "false",
            "no_cache": "true",
        }
        self.search = GoogleSearch(self.params)
        self.trends = []
        self.last_trend_execution = datetime.now(timezone.utc)
        self.config = get_config(settings.config_id)
        self._retrieve_trends()

    def get_trends(self) -> list[Trend]:
        return self.trends

    def _retrieve_trends(self):
        error = "Something went wrong"
        results = self.search.get_dict()
        counter = 1
        for trend in results["trending_searches"]:
            if not self._is_blacklisted(trend["categories"]):
                keywords = trend.get("trend_breakdown", None)
                end_ts = trend.get("end_timestamp")
                start_ts = trend.get("start_timestamp")
                trend = Trend(
                    id=counter,
                    trend=trend.get("query", error),
                    search_volume=trend.get("search_volume", error),
                    increase=trend.get("increase_percentage", error),
                    keywords=keywords,
                    started_at=datetime.fromtimestamp(start_ts, tz=timezone.utc)
                    if start_ts is not None
                    else None,
                    finished_at=datetime.fromtimestamp(end_ts, tz=timezone.utc)
                    if end_ts is not None
                    else None,
                    is_active=trend["active"],
                )
                self.trends.append(trend)
                counter += 1

    def _is_blacklisted(self, category_names):
        for cat in [c["name"].lower() for c in category_names]:
            if any(b in cat for b in self.config.trend_filter):
                return True
        return False
