from pathlib import Path
import ollama
import json

from constants import PHRASES
from chat_composer import compose_chat_from_data

path_to_data = Path("data") / "animal_food"
train_file = "train.json"
with (path_to_data / train_file).open("r") as file:
    train_data = json.load(file)
    train_data = train_data[PHRASES]

options = {
    "seed": 101,
    "temperature": 0
}

intro_chat = {
    "role": "user",
    "content": "Answer every message with either 'animal' or 'food'",
}
train_chat = compose_chat_from_data(train_data)
test_chat = {
    "role": "user",
    "content": "As sly as a fox.",
}
complete_chat = [
    intro_chat,
    *train_chat,
    test_chat,
]

response = ollama.chat(
    model="llama2-uncensored",
    messages=complete_chat,
)
print(response["message"]["content"])
