import pytest 
from unittest.mock import MagicMock
import src.nodes.news_scrapers as ns
from src.nodes.graph_state import get_empty_state_voids


@pytest.fixture(autouse=True)
def mock_newspaper(monkeypatch):
    newspaper_mock = MagicMock(autospec=ns.newspaper)
    monkeypatch.setattr(ns, "newspaper", newspaper_mock)
    return newspaper_mock


@pytest.fixture(autouse=True)
def mock_article(monkeypatch):
    article_mock = MagicMock(autospec=ns.Article)
    monkeypatch.setattr(ns, "Article", article_mock)
    return article_mock


def test_get_newspapers_news(monkeypatch):
    papers = [
        {}
    ]
    nn = ns.GetNewspaperNews()
    result = nn(get_empty_state_voids())
    