import pytest

from src.llm import OllamaInterface


@pytest.fixture
def interface():  # noqa: D103
    return OllamaInterface("llama2-uncensored")

def test_keep_alive(interface):  # noqa: D103
    result = interface.keep_alive()
    assert result is not None

def test_append_context(interface):  # noqa: D103
    interface.append_context("Test context")
    assert "Test context" in interface.context

def test_submit_query(interface):  # noqa: D103
    response = interface.submit_query("Hello")
    assert isinstance(response, str)