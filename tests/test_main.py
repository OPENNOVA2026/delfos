import pytest
from unittest.mock import mock_open
import json
from src.main import run
from src import main
from datetime import datetime


@pytest.fixture(autouse=True)
def mock_pipeline_instance(mocker):
    mock_pipeline_class = mocker.patch("src.main.DelfosVoidPipeline")
    mock_instance = mock_pipeline_class.return_value
    mock_instance.state = {"key": "value", "number": 123}
    return mock_instance

@pytest.fixture(autouse=True)
def mock_file(mocker):
    mock_file = mock_open()
    mocker.patch("builtins.open", mock_file)
    return mock_file


def test_run_calls_pipeline_workflow(mock_pipeline_instance):
    run()
    mock_pipeline_instance.run_workflow.assert_called_once()


def test_run_writes_file_in_local_environment(monkeypatch, mock_file):

    run()
    mock_file.assert_called_once_with("./test.json", "w")
    
    expected_json = json.dumps(
        {"key": "value", "number": 123}, 
        indent=2, 
        ensure_ascii=False, 
        default=str
    )
    mock_file().write.assert_called_once_with(expected_json)


def test_run_does_not_write_file_in_prod_environment(monkeypatch, mock_file):
    monkeypatch.setattr(main.settings, "environment", "test")  
    run()
    mock_file.assert_not_called()


def test_run_handles_non_serializable_state(mock_file, mock_pipeline_instance):
    mock_pipeline_instance.state = {
        "timestamp": datetime(2025, 1, 1, 12, 0, 0),
        "data": "test"
    }
    
    run()
    
    assert mock_file().write.called
    written_content = mock_file().write.call_args[0][0]
    assert "2025-01-01 12:00:00" in written_content