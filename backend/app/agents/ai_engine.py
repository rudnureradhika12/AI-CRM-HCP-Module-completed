import os
import requests
from openai import OpenAI

USE_GROQ = True   # set False for OpenAI

def run_ai(prompt):

    if USE_GROQ:
        return groq_ai(prompt)
    else:
        return openai_ai(prompt)


def openai_ai(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user","content":prompt}]
    )
    return res.choices[0].message.content


def groq_ai(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama3-8b-8192",
        "messages": [{"role":"user","content": prompt}]
    }

    res = requests.post(url, json=body, headers=headers)
    return res.json()["choices"][0]["message"]["content"]
