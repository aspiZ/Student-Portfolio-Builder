from google import genai
import os

MODEL_NAME = "gemini-3-flash-preview"

GEMINI_API_KEY = os.getenv("")

def generate_text(prompt: str) -> str:
    api_key = GEMINI_API_KEY

    if not api_key:
        return "GEMINI_API_KEY недостасува или е погрешен"

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return (response.text or "").strip() or "Нема резултат од AI (празен текст)."
    except Exception as e:
        return f"AI грешка: {e}"

