import pytest
from unittest.mock import MagicMock
import src.nodes.voids_nodes as vn
from src.nodes.voids_nodes import RetrieveTrends
from src.nodes.graph_state import get_empty_state_voids
from datetime import datetime
from src.domain.models import Trend


state = get_empty_state_voids(last_ingested_datetime=datetime(year=2026, month=1, day=2, hour=8, minute=30))

trend_list = [
    Trend(
        trend="trend_1",
        id=1,
        search_volume=300,
        increase=20,
        is_active=True,
        started_at= datetime(year=2026, month=1, day=2, hour=6, minute=30)
    ),
    Trend(
        trend="trend_2",
        id=2,
        search_volume=300,
        increase=20,
        is_active=True,
        started_at= datetime(year=2026, month=1, day=2, hour=10, minute=30)
    ),
    Trend(
        trend="trend_3",
        id=3,
        search_volume=300,
        increase=20,
        is_active=False,
        started_at=datetime(year=2026, month=1, day=1, hour=20, minute=30),
        finished_at=datetime(year=2026, month=1, day=2, hour=11, minute=0)
    ),
    Trend(
        trend="trend_4",
        id=4,
        search_volume=300,
        increase=20,
        is_active=False,
        started_at=datetime(year=2026, month=1, day=2, hour=9, minute=45),
        finished_at=datetime(year=2026, month=1, day=2, hour=13, minute=10)
    ),
    Trend(
        trend="trend_5",
        id=5,
        search_volume=300,
        increase=20,
        is_active=False,
        started_at=datetime(year=2026, month=1, day=1, hour=20, minute=35),
        finished_at=datetime(year=2026, month=1, day=2, hour=7, minute=20)
    )
]


def test_retrieve_trends(monkeypatch):
    get_trends_cls_mocked = MagicMock(autospec=vn.SearchTrends)
    get_trends_mocked = get_trends_cls_mocked.return_value
    get_trends_mocked.get_trends.return_value = trend_list
    monkeypatch.setattr(vn, "SearchTrends", get_trends_cls_mocked)
    
    rt = RetrieveTrends()
    result = rt(state)
    
    assert len(result["trends"]) == 4
    assert "last_trend_execution" in result