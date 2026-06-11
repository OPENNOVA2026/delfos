import json
import pytest



@pytest.fixture(autouse=True)
def fake_config_json(monkeypatch, tmp_path):
    fake_config = {
        "1": {
            "description": "Test config",
            "news_origin": [
                {"name": "Paper1", "url": "https://paper1.com", "lang": "es"},
                {"name": "Paper2", "url": "https://paper2.com", "lang": "es"},
                {"name": "Paper3", "url": "https://paper3.com", "lang": "es"},
                {"name": "Paper4", "url": "https://paper4.com", "lang": "es"},
            ],
            "skip_urls": [],
            "trend_filter": ["movies", "games", "entertainment"],
        }
    }

    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(fake_config), encoding="utf-8")

    monkeypatch.chdir(tmp_path)


@pytest.fixture(autouse=True)
def test_env_set(monkeypatch):
    env = {
        "ENVIRONMENT": "test",
        "AZURE_OPENAI_ENDPOINT": "https://aoai.fake.com/",
        "AZURE_OPENAI_API_KEY": "fake_azure_api_key",
        "OPENAI_API_VERSION": "fake_azure_api_version",
        "DEBUG": "false",
        "CELERY_BROKER_URL": "fakedis://fakedis:1234/0",
        "FAKE_EMAIL": "False",
        "SMTP_HOST": "smtp.fake.com",
        "SMTP_PORT": "1234",
        "SMTP_SENDER": "fakencio@fake.com",
        "SMTP_USER": "fakencio@fake.com",
        "SMTP_PASSWORD": "fake smtp password",
        "LOCAL": "True",
        "EMAIL_LIST": "fakencioprimero@fake.es,fakenciosegundo@fake.es",
        "SERPAPI_KEY": "fake_serpapi_key",
    }

    for key, value in env.items():
        monkeypatch.setenv(key, value)