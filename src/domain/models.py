from datetime import datetime
from typing import Any

from pydantic import BaseModel


class TrendNotification(BaseModel):
    trend: str
    volume: int
    growth: int
    started_at: datetime
    finished_at: datetime | None
    news_path: str | None = None
    keywords: list[str] | None
    ivs: float | None = None
    demand_factor: float | None = None
    coverage_factor: float | None = None
    delay_factor: float | None = None
    plurality_factor: float | None = None
    news_summary: str | None = None


class ExternalNotificationRequest(BaseModel):
    last_trend_execution: datetime
    infovoids: list[TrendNotification]


class Trend(BaseModel):
    id: int
    trend: str
    search_volume: int
    increase: int
    keywords: list[str] | None = None
    is_active: bool
    started_at: datetime
    finished_at: datetime | None = None
    ivs: float | None = None
    demand_factor: float | None = None
    coverage_factor: float | None = None
    delay_factor: float | None = None
    plurality_factor: float | None = None
    news: list[dict[str, Any]] = []
    news_summary: str | None = None
    category: str = "unknown"
