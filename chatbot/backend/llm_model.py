import os
import requests
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def query_llama(prompt: str) -> str:
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama-3.1-8b-instant",
    )
    return chat_completion.choices[0].message.content




