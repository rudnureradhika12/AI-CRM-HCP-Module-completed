import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_ai_reply(message: str):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are an AI CRM assistant for doctors and HCP interactions."},
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]
