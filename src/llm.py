import ollama

"""
from ollama import chat

# Define the model and the message
model_name = 'llama3.2'
messages = [
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    },
]

# Send the message using the chat function
response = chat(model=model_name, messages=messages)

# Access and print the response content
print(response.message.content)
"""


class OllamaInterface:
    """_summary_."""

    def __init__(self, model_name: str):  # noqa: D107
        self.model_name = model_name
        self.context = ""
        # Optionally pre-load model or store a handle
        self.client = ollama.Client(model=self.model_name)

    def keep_alive(self):  # noqa: D102
        # Simple method to ensure model remains loaded
        response = self.client.generate("ping")
        return response

    def submit_query(self, prompt: str) -> str:  # noqa: D102
        # Combine stored context with new prompt
        combined_prompt = f"{self.context}\n{prompt}"
        response = self.client.generate(combined_prompt)
        return response.get("text", "")

    def append_context(self, additional_context: str):  # noqa: D102
        # Adds new context to be used in subsequent queries
        self.context += "\n" + additional_context