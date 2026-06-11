import pytest
from unittest.mock import MagicMock

import src.clients.external_client as ec 
from src.clients.external_client import ExternalClient
from src.domain.models import Trend
from datetime import datetime

last_ingested_datetime=datetime(year=2026, month=1, day=2, hour=8, minute=30)

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



def test_external_client(monkeypatch):

    req_mock = MagicMock(autospec=ec.requests)
    monkeypatch.setattr(ec, "requests", req_mock)
    
    expected_infovoids = [
        {
            "trend": t.trend,
            "volume": t.search_volume,
            "growth": t.increase,
            "started_at": t.started_at.isoformat(),
            "finished_at": t.finished_at.isoformat() if t.finished_at else None,
            "news_path": "s3_path/file",
            "keywords": t.keywords,
            "ivs": t.ivs,
            "demand_factor": t.demand_factor,
            "coverage_factor": t.coverage_factor,
            "delay_factor": t.delay_factor,
            "plurality_factor": t.plurality_factor,
            "news_summary": t.news_summary,
        }
        for t in trend_list
    ]
    
    expected_payload = {
        "last_trend_execution": last_ingested_datetime.isoformat(),
        "infovoids": expected_infovoids,
    }
    
    client = ExternalClient()
    client.send_info_voids(trend_list, last_ingested_datetime, "s3_path/file")
    
    req_mock.post.assert_called_once_with("", json=expected_payload)