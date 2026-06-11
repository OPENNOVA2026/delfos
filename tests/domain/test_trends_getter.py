import pytest
from unittest.mock import MagicMock
from src.domain.trends_getter import SearchTrends
import src.domain.trends_getter as tg


trending_searches = {
    "trending_searches": [
        {
            "query": "trend_1",
            "search_volume": 300,
            "increase_percentage": 30,
            "start_timestamp": 1234,
            "end_timestamp": 3456,
            "active": False,
            "categories": [{"name": "Games and Entertainment"}, {"name": "Politics"}]
        },
        {
            "query": "trend_2",
            "search_volume": 300,
            "increase_percentage": 30,
            "start_timestamp": 1234,
            "end_timestamp": None,
            "active": True,
            "categories": [{"name": "Movies"}, {"name": "Film"}]
        },
        {
            "query": "trend_3",
            "search_volume": 300,
            "increase_percentage": 30,
            "start_timestamp": 1234,
            "end_timestamp": 3456,
            "active": False,
            "categories": [{"name": "Health"}]
        },
        {
            "query": "trend_4",
            "search_volume": 300,
            "increase_percentage": 30,
            "start_timestamp": 1234,
            "end_timestamp": None,
            "active": True,
            "categories": [{"name": "Economy"}, {"name": "Politics"}]
        }
    ]
}


@pytest.fixture(autouse=True)
def mock_google_search(monkeypatch):
    google_search_cls_mock = MagicMock(autospec=tg.GoogleSearch)
    google_search_mock = google_search_cls_mock.return_value
    google_search_mock.get_dict.return_value = trending_searches
    monkeypatch.setattr(tg, "GoogleSearch", google_search_cls_mock)
    return google_search_mock


def test_trends_getter(mock_google_search):
    st = SearchTrends()
    
    trends = st.get_trends()
    
    mock_google_search.get_dict.assert_called_once()
    assert len(trends) == 2
    assert trends[0].trend == "trend_3"
    assert trends[1].trend == "trend_4"