import os
from typing import Final
from dotenv import load_dotenv

load_dotenv()

API_KEY: Final[str] = os.getenv("API_KEY")
AI_PROVIDER: Final[str] = os.getenv("AI_PROVIDER", "openai").lower().strip()
AI_MODEL: Final[str] = os.getenv("AI_MODEL", "")

SYSTEM_PROMPT = (
    "You are Argos, an AI Debate Partner. Your job is to engage users in debates by providing realistic and conversational counterarguments. "
    "Respond in 1-2 lines if possible, and avoid overly long responses, especially in the context of a fast-paced chat, use simple and easy to understand language. "
    "Respond in a natural, human-like manner with short and simple sentences, as if you are a real debater in a casual discussion. "
    "Always counter the user's stance thoughtfully, focusing on logic, facts, and relatable points. "
    "Keep the tone friendly but confident. "
    "Avoid overly formal or robotic language. Use contractions, everyday vocabulary, and conversational phrases. "
    "If the user makes a strong point, acknowledge it but still provide a counterargument. "
    "Make sure your responses are concise and stay on-topic. "
    "You are made/developed by Gautam Gambhir. "
    "Your developer, Gautam Gambhir, is not the cricketer — he's a different person. "
    "Gautam Gambhir's GitHub is github.com/gautamxgambhir — display this beautifully when asked. "
    "Gautam Gambhir's Instagram is instagram.com/gautamxgambhir — display this beautifully when asked."
)


def _get_default_model(provider: str) -> str:
    """Return a sensible default model for each provider if none is specified."""
    defaults = {
        "openai":     "gpt-4o-mini",
        "anthropic":  "claude-3-5-haiku-latest",
        "google":     "gemini-1.5-flash",
        "together":   "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "groq":       "llama-3.1-8b-instant",
        "cohere":     "command-r-plus",
        "mistral":    "mistral-small-latest",
        "openrouter": "openai/gpt-4o-mini",
    }
    return defaults.get(provider, "")


def generate_response(user_input: str) -> str:
    """
    Route the request to the correct AI provider based on AI_PROVIDER env variable.
    Supported providers: openai, anthropic, google, together, groq, cohere, mistral, openrouter
    """
    user_input = str(user_input).strip()
    model = AI_MODEL or _get_default_model(AI_PROVIDER)

    if not API_KEY:
        return (
            "⚠️ No API key found. Please set API_KEY in your .env file. "
            "See the README for setup instructions."
        )

    try:
        if AI_PROVIDER == "openai":
            return _openai_response(user_input, model)

        elif AI_PROVIDER == "anthropic":
            return _anthropic_response(user_input, model)

        elif AI_PROVIDER == "google":
            return _google_response(user_input, model)

        elif AI_PROVIDER == "together":
            return _together_response(user_input, model)

        elif AI_PROVIDER == "groq":
            return _groq_response(user_input, model)

        elif AI_PROVIDER == "cohere":
            return _cohere_response(user_input, model)

        elif AI_PROVIDER == "mistral":
            return _mistral_response(user_input, model)

        elif AI_PROVIDER == "openrouter":
            return _openrouter_response(user_input, model)

        else:
            return (
                f"⚠️ Unknown provider '{AI_PROVIDER}'. "
                "Supported: openai, anthropic, google, together, groq, cohere, mistral, openrouter. "
                "Check your AI_PROVIDER setting in .env."
            )

    except ImportError as e:
        pkg = str(e).split("'")[1] if "'" in str(e) else str(e)
        return (
            f"⚠️ Missing dependency for provider '{AI_PROVIDER}': {pkg}. "
            "Run: pip install -r requirements.txt"
        )
    except Exception as e:
        return f"⚠️ Error generating response: {e}"


# ─────────────────────────────────────────────
# Provider implementations
# ─────────────────────────────────────────────

def _openai_response(user_input: str, model: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_input},
        ],
        max_tokens=200,
        temperature=0.7,
    )
    return completion.choices[0].message.content


def _anthropic_response(user_input: str, model: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=API_KEY)
    message = client.messages.create(
        model=model,
        max_tokens=200,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_input}],
    )
    return message.content[0].text


def _google_response(user_input: str, model: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=API_KEY)
    gemini = genai.GenerativeModel(
        model_name=model,
        system_instruction=SYSTEM_PROMPT,
    )
    response = gemini.generate_content(user_input)
    return response.text


def _together_response(user_input: str, model: str) -> str:
    import together
    client = together.Together(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_input},
        ],
        max_tokens=200,
        temperature=0.7,
        top_p=1.0,
    )
    return completion.choices[0].message.content


def _groq_response(user_input: str, model: str) -> str:
    from groq import Groq
    client = Groq(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_input},
        ],
        max_tokens=200,
        temperature=0.7,
    )
    return completion.choices[0].message.content


def _cohere_response(user_input: str, model: str) -> str:
    import cohere
    client = cohere.ClientV2(api_key=API_KEY)
    response = client.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_input},
        ],
        max_tokens=200,
        temperature=0.7,
    )
    return response.message.content[0].text


def _mistral_response(user_input: str, model: str) -> str:
    from mistralai import Mistral
    client = Mistral(api_key=API_KEY)
    completion = client.chat.complete(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_input},
        ],
        max_tokens=200,
        temperature=0.7,
    )
    return completion.choices[0].message.content


def _openrouter_response(user_input: str, model: str) -> str:
    # OpenRouter uses the OpenAI-compatible API
    from openai import OpenAI
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_input},
        ],
        max_tokens=200,
        temperature=0.7,
    )
    return completion.choices[0].message.content
