# app/parsing/base/gemini_client.py
import os
import time
import google.generativeai as genai
from dotenv import load_dotenv
from app.core.gemini_rate_limiter import GeminiRateLimiter

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

rate_limiter = GeminiRateLimiter(rate_limit_per_minute=60)

def send_prompt(prompt: str, usage_key: str = "default", retries: int = 5) -> str:
    for attempt in range(retries):
        try:
            rate_limiter.wait(usage_key)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"[Gemini Attempt {attempt+1} | Key: {usage_key}] Error: {e}", flush=True)
            if attempt == retries - 1:
                raise
            time.sleep(2)
