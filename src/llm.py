import json
from typing import AnyStr, Optional

import ollama
import requests

OLLAMA_ADDRESS = "localhost"
OLLAMA_PORT = "11434"
DEFAULT_ANSWER = "I could not generate a reply."

# These are only used if the chat http method is used
STANDARD_HTTP_LLM_SETTINGS = {
    "temperature": 0.1,
    "seed": 0,
    "stream": False,
}


class OllamaServerError(Exception):  # noqa: D101
    pass


class ModelNotAvailableError(Exception):  # noqa: D101
    pass


class Llm:
    """The LLM interface.

    This class assumes ollama is running in the background,
    which is a local LLM server. The class then provides an
    interface for interacting with the service.
    """

    def __init__(self, model_name: str, system_message: Optional[AnyStr] = None):
        """Store the model name if everything is fine."""
        if not self._is_ollama_running():
            raise OllamaServerError("Ollama server is not running.")
        if not self._is_model_available(model_name):
            raise ModelNotAvailableError(f"Model '{model_name}' is not available.")
        self.model_name = model_name
        self.system_message = system_message

    @staticmethod
    def _is_ollama_running():
        """Check if the ollama server is running."""
        successful_response = 200
        try:
            response = requests.get(f"http://{OLLAMA_ADDRESS}:{OLLAMA_PORT}/")
            return response.status_code == successful_response
        except requests.exceptions.ConnectionError:
            return False

    @staticmethod
    def _is_model_available(model_name):
        """Check if the model is available in the server."""
        models = ollama.list().models
        model_names = [model.model for model in models]
        return model_name in model_names

    def chat(self, input_text: str) -> str:
        """Chat with the LLM with no context."""
        message = [
            {
                "role": "user",
                "content": input_text,
            }
        ]
        if self.system_message:
            message = Llm._prepend_system_message(self.system_message, message)
        response = ollama.chat(model=self.model_name, messages=message)
        if response.message.content:
            return response.message.content
        else:
            return DEFAULT_ANSWER

    @staticmethod
    def _prepend_system_message(system_message, message):
        """Prepend a system message to the existing message if needed."""
        formatted_system_message = {
            "role": "system",
            "content": system_message,
        }
        return [formatted_system_message, *message]

    def _extract_message(self, http_response: requests.Response) -> str:
        """Extract the message content from the HTTP response."""
        response_text = http_response.text.strip()
        response_jsons = response_text.split("\n")
        message_bits = []
        for response_json in response_jsons:
            parsed_json = json.loads(response_json)
            if "message" in parsed_json and "content" in parsed_json["message"]:
                message_bits.append(parsed_json["message"]["content"])
        message = "".join(message_bits)
        return message

    def chat_http(self, input_text: str, **kwargs) -> str:
        """Chat with the LLM using HTTP POST request with no context."""
        message = [
            {
                "role": "user",
                "content": input_text,
            }
        ]
        if self.system_message:
            message = Llm._prepend_system_message(self.system_message, message)
        url = f"http://{OLLAMA_ADDRESS}:{OLLAMA_PORT}/api/chat"
        payload = {
            "model": self.model_name,
            "messages": message,
        }
        # append standard settings and add any extra setting passed as a parameter
        # NB the kwargs have the power to overwrite the standard settings
        payload = payload | STANDARD_HTTP_LLM_SETTINGS
        payload.update(kwargs)
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return self._extract_message(response)
        except requests.exceptions.RequestException:
            return DEFAULT_ANSWER

    def chat_with_history(self, history: list[str], input_text: str) -> str:
        """Chat with the LLM with context.

        Args:
            history (list[str]): assumed to be a list of alternating messages:
                                 one from the user, then the assistant, then user, etc.
            input_text (str): the new query to be answered by the model.
        """
        Llm._validate_history(history)

        # apply a user/assistant and content pattern to the history
        formatted_history = []
        roles = ["user", "assistant"]
        for i, content in enumerate(history):
            role = roles[i % 2]
            formatted_history.append({"role": role, "content": content})
        # compose final message and submit it to the server
        message = formatted_history + [
            {
                "role": "user",
                "content": input_text,
            },
        ]
        if self.system_message:
            message = Llm._prepend_system_message(self.system_message, message)
        response = ollama.chat(model=self.model_name, messages=message)
        if response.message.content:
            return response.message.content
        else:
            return DEFAULT_ANSWER

    @staticmethod
    def _validate_history(history: list[str]):
        """Check if the history is valid.

        Args:
            history (list[str]): assumed to be a list of alternating messages:
                                 one from the user, then the assistant, then user, etc.

        Raises:
            ValueError: If the history is not a list of strings or if it does not contain
                        an even number of elements.
        """
        if not isinstance(history, list) or not all(isinstance(item, str) for item in history):
            raise ValueError("History must be a list of strings.")
        if len(history) % 2 != 0:
            raise ValueError("History must contain an even number of elements.")
