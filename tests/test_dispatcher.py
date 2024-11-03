import pytest

from src.dispatcher import Dispatcher


def test_llm_settings_check():
    incomplete_settings = {"llm_model": "llama2-uncensored"}
    with pytest.raises(KeyError):
        Dispatcher(incomplete_settings)

    wrong_settings = {"llllm_model": "llama2-uncensored"}
    with pytest.raises(KeyError):
        Dispatcher(wrong_settings)

    # too_many_settings = {
    #     "llm_model": "llama2-uncensored",
    #     "temp": 0.1,
    #     "seed": 1,
    #     "day": "Monday",
    # }
    # with pytest.raises(KeyError):
    #     Dispatcher(too_many_settings)


def test_register_person():
    pass
