import pytest
import requests

from src.llm import Llm


@pytest.fixture(scope="module")
def llm_instance():  # noqa: D103
    return Llm("llama2-uncensored:latest")


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


def test_validate_history_valid(llm_instance):
    """Test _validate_history with valid history."""
    valid_history = ["user message", "assistant message", "user message", "assistant message"]
    try:
        llm_instance._validate_history(valid_history)
    # fail the test if an error is raised (the history is valid)
    except ValueError:
        pytest.fail("_validate_history raised ValueError unexpectedly!")


def test_validate_history_invalid_type(llm_instance):
    """Test _validate_history with invalid history type."""
    invalid_history = "this is not a list"
    with pytest.raises(ValueError, match="History must be a list of strings."):
        llm_instance._validate_history(invalid_history)


def test_validate_history_invalid_elements(llm_instance):
    """Test _validate_history with invalid history elements."""
    invalid_history = ["user message", 123, "user message", "assistant message"]
    with pytest.raises(ValueError, match="History must be a list of strings."):
        llm_instance._validate_history(invalid_history)


def test_validate_history_odd_length(llm_instance):
    """Test _validate_history with odd number of history elements."""
    invalid_history = ["user message", "assistant message", "user message"]
    with pytest.raises(ValueError, match="History must contain an even number of elements."):
        llm_instance._validate_history(invalid_history)


# def test_keep_alive(interface):  # noqa: D103
#     result = interface.keep_alive()
#     assert result is not None

# def test_append_context(interface):  # noqa: D10
#     interface.append_context("Test context")
#     assert "Test context" in interface.context

# def test_submit_query(interface):  # noqa: D103
#     response = interface.submit_query("Hello")
#     assert isinstance(response, str)
