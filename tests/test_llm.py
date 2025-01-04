import pytest
import requests

from src.llm import Llm


@pytest.fixture(scope="module")
def llm_instance():  # noqa: D103
    return Llm("llama2-uncensored")

def mock_get_success(_):
    """Mock a successful GET request."""
    class MockResponse:
        status_code = 200
    return MockResponse()

def mock_get_failure(_):
    """Mock a failed GET request."""
    raise requests.exceptions.ConnectionError

def test_is_ollama_running_success(monkeypatch, llm_instance):
    """Test if the OLLAMA server is running."""
    monkeypatch.setattr(requests, "get", mock_get_success)
    assert llm_instance._is_ollama_running() is True

def test_is_ollama_running_failure(monkeypatch, llm_instance):
    """Test if the OLLAMA server is not running."""
    monkeypatch.setattr(requests, "get", mock_get_failure)
    assert llm_instance._is_ollama_running() is False

# def test_keep_alive(interface):  # noqa: D103
#     result = interface.keep_alive()
#     assert result is not None

# def test_append_context(interface):  # noqa: D10
#     interface.append_context("Test context")
#     assert "Test context" in interface.context

# def test_submit_query(interface):  # noqa: D103
#     response = interface.submit_query("Hello")
#     assert isinstance(response, str)