import ollama
import requests
from ollama import chat

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

OLLAMA_ADDRESS = "localhost"
OLLAMA_PORT = "11434"

class Llm:
    """The LLM interface.
    
    This class assumes ollama is running in the background, 
    which is a local LLM server. The class then provides an 
    interface for interacting with the service.
    """

    def __init__(self, model_name: str):  
        """Check if ollama is running and if the desired model is available."""  
        self.model_name = model_name
        # self.context = ""
        # Optionally pre-load model or store a handle
        # self.client = ollama.Client(model=self.model_name)

    def _is_ollama_running(self):
        """Check if the ollama server is running."""
        successful_response = 200
        try:
            response = requests.get(f"http://{OLLAMA_ADDRESS}:{OLLAMA_PORT}/")
            return response.status_code == successful_response
        except requests.exceptions.ConnectionError:
            return False

    def _is_model_available(self):
        """Check if the model is available in the server."""
        models = ollama.list().models
        model_names = [model.model for model in models]
        return self.model_name in model_names
    
    def keep_alive(self):
        pass

    # def submit_query(self, prompt: str) -> str:  # noqa: D102
    #     # Combine stored context with new prompt
    #     combined_prompt = f"{self.context}\n{prompt}"
    #     response = self.client.generate(combined_prompt)
    #     return response.get("text", "")

    # def append_context(self, additional_context: str):  # noqa: D102
    #     # Adds new context to be used in subsequent queries
    #     self.context += "\n" + additional_context