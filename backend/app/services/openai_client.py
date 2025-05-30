from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import os


def generate_text(prompt):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
