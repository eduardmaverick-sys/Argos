from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

key = os.getenv("API_KEY", "").strip()

print("Provider:", os.getenv("AI_PROVIDER"))
print("Model:", os.getenv("AI_MODEL"))
print("Key loaded:", bool(key))
print("Key prefix:", key[:10])
print("Key length:", len(key))

client = OpenAI(
    api_key=key,
    base_url="https://openrouter.ai/api/v1",
)

try:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {"role": "user", "content": "Say hello in one sentence."}
        ],
    )

    print("\nSUCCESS:")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nFAILED:")
    print(type(e).__name__)
    print(e)