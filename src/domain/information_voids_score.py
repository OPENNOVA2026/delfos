from __future__ import annotations

import math
from collections import Counter
from datetime import datetime
from typing import TypedDict

from domain.models import Trend
from src.core.config import get_config
from src.core.settings import settings


class IVSResult(TypedDict):
    ivs: float
    demand_factor: float
    coverage_factor: float
    delay_factor: float
    plurality_factor: float  # diversity score in [0,1]


class InformationVoidsScore:
    """
    Compute Information Void Score (IVS) for a Trend.

    IVS = w1 * demand
        + w2 * (1 - coverage)
        + w3 * delay
        + w4 * (1 - plurality)

    All sub-scores are in [0,1]. Higher IVS => bigger information void.
    """

    def __init__(
        self,
        w1: float = 0.25,
        w2: float = 0.35,
        w3: float = 0.25,
        w4: float = 0.15,
        news_per_hund: int = 1,
        max_time_offset: int = 720,  # minutes
        use_log_demand: bool = False,
        use_entropy_plurality: bool = True,
        delay_quantile: float = 0.25,  # 0 -> earliest, 0.5 -> median
    ):
        self.config = get_config(settings.config_id)
        assert abs((w1 + w2 + w3 + w4) - 1.0) < 1e-9, "Weights must sum to 1."
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.w4 = w4
        self.news_per_hund = news_per_hund
        self.max_time_offset = max_time_offset
        self.use_log_demand = use_log_demand
        self.use_entropy_plurality = use_entropy_plurality
        self.delay_quantile = delay_quantile
        self.news_sources_total = len(self.config.news_origin)

    def evaluate(self, topic: Trend) -> IVSResult:
        demand = self.demand_factor(topic.search_volume)
        coverage = self.coverage_factor(topic.news, topic.search_volume)
        delay = self.delay_factor(topic.news, topic.started_at)
        plurality = self.plurality_factor(topic.news)

        ivs = (
            self.w1 * demand
            + self.w2 * (1 - coverage)
            + self.w3 * delay
            + self.w4 * (1 - plurality)
        )
        # Cap to [0,1] for safety (weights sum to 1, but numeric drift)
        ivs = max(0.0, min(1.0, ivs))

        return {
            "ivs": ivs,
            "demand_factor": demand,
            "coverage_factor": coverage,
            "delay_factor": delay,
            "plurality_factor": plurality,
        }

    def demand_factor(self, searches: int) -> float:
        if searches <= 0:
            return 0.0
        if self.use_log_demand:
            # More stable across orders of magnitude
            return min(1.0, math.log1p(searches) / math.log1p(1_000_000))
        return min(1.0, searches / 100_000)

    def coverage_factor(self, articles: list[dict], searches: int) -> float:
        expected = (self.news_per_hund * max(0, searches)) / 1_000
        if expected <= 0:
            return 0.0
        actual = sum(1 for a in articles if a.get("published_at"))
        return min(1.0, actual / expected)

    def delay_factor(self, articles: list[dict], trend_start: datetime) -> float:
        # Collect valid times strictly after trend_start
        ts0 = trend_start.replace(tzinfo=None)
        times = []
        for a in articles:
            dt = a.get("published_at")
            if isinstance(dt, datetime):
                dt0 = dt.replace(tzinfo=None)
                if dt0 > ts0:
                    times.append(dt0)

        if not times:
            # No coverage after trend start -> maximal delay signal
            return 1.0

        # Choose earliest / quantile / median to be robust to outliers
        times.sort()
        idx = max(0, min(len(times) - 1, int(self.delay_quantile * (len(times) - 1))))
        chosen = times[idx]

        minutes = (chosen - ts0).total_seconds() / 60.0
        if minutes <= 0:
            return 0.0
        return min(1.0, minutes / self.max_time_offset)

    def plurality_factor(self, articles: list[dict]) -> float:
        if self.use_entropy_plurality:
            origins = [a.get("origin") for a in articles if a.get("origin")]
            if not origins:
                return 0.0

            origin_counts = Counter(origins)
            distinct_origins = len(origin_counts)
            n_origins_total = sum(origin_counts.values())
            if distinct_origins <= 1:
                return 0.0

            origin_probabilities = [
                origin_frequency / n_origins_total
                for origin_frequency in origin_counts.values()
            ]
            entropy = -sum(prob * math.log(prob) for prob in origin_probabilities)
            plurality = entropy / math.log(self.news_sources_total)  # [0,1]

            return plurality

        # Simple distinct-sources over total possible sources
        distinct = len({a.get("origin") for a in articles if a.get("origin")})
        total = self.news_sources_total if self.news_sources_total is not None else 0
        if total <= 0:
            return max(0.0, min(1.0, (distinct - 1) / 2)) if distinct > 0 else 0.0
        return max(0.0, min(1.0, distinct / total))
