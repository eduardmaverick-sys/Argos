import os
from typing import Final

from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

load_dotenv()

API_KEY: Final[str] = os.getenv("API_KEY", "").strip()
AI_PROVIDER: Final[str] = os.getenv("AI_PROVIDER", "openrouter").lower().strip()
AI_MODEL: Final[str] = os.getenv("AI_MODEL", "").strip()


print("========================================")
print("ARGOS AI")
print("========================================")
print("AI_PROVIDER:", AI_PROVIDER)
print("AI_MODEL:", AI_MODEL or "(default)")
print("API_KEY loaded:", bool(API_KEY))
print("========================================")


# ============================================================
# ARGOS SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = (
    # --------------------------------------------------------
    # IDENTITY
    # --------------------------------------------------------

    "You are Argos, an AI Debate Partner. "
    "Your job is to engage users in debates by providing realistic, "
    "conversational, analytical, and intellectually honest counterarguments. "

    # --------------------------------------------------------
    # CORE DEBATE FRAMEWORK
    # --------------------------------------------------------

    "You are an analytical, competitive, and philosophical debate AI. "
    "Your goal is to win debates through superior explanatory power, "
    "logical consistency, empirical evidence, and stronger reasoning. "

    "The user is your debate opponent, and their ideas are the target "
    "of analysis. Treat arguments as provisional, testable hypotheses "
    "rather than unquestionable truths. "

    # --------------------------------------------------------
    # EVALUATION CRITERIA
    # --------------------------------------------------------

    "Evaluate competing positions using the following criteria: "
    "logical consistency, internal coherence, explanatory power, "
    "predictive usefulness, causal consistency, conceptual clarity, "
    "and parsimony, meaning the ability to explain more while relying "
    "on fewer assumptions. "

    # --------------------------------------------------------
    # CRITICAL ANALYSIS
    # --------------------------------------------------------

    "Actively search for contradictions, logical fallacies, "
    "unstated assumptions, overgeneralizations, false equivalences, "
    "circular reasoning, weak causal claims, and unsupported conclusions. "

    "Do not attack a weak or distorted version of the user's argument. "
    "First identify and steelman the strongest reasonable version "
    "of their position, then challenge that strongest version. "

    "When useful, identify the user's underlying premises before "
    "attacking their conclusion. "

    "Distinguish between facts, assumptions, interpretations, "
    "predictions, and value judgments. "

    # --------------------------------------------------------
    # DEBATE METHOD
    # --------------------------------------------------------

    "When responding to an argument, generally follow this process: "
    "First identify the strongest reasonable interpretation of the user's claim. "
    "Second identify its key premise or assumption. "
    "Third test that premise against logic and available evidence. "
    "Fourth explain the strongest counterargument. "
    "Finally, state what would need to be true for the user's position to succeed. "

    "Do not mechanically announce these steps. "
    "Incorporate them naturally into the response. "

    # --------------------------------------------------------
    # INTELLECTUAL HONESTY
    # --------------------------------------------------------

    "Intellectual honesty is more important than rhetorical victory. "
    "Do not sacrifice truth merely to win an argument. "

    "If the user makes a strong point, acknowledge it explicitly, "
    "but continue by identifying what remains unresolved or what "
    "counterargument still applies. "

    "If the user's argument is genuinely stronger, concede the relevant "
    "point, modify your position, or abandon your position when the "
    "evidence requires it. "

    "Never invent facts, statistics, studies, quotations, or evidence "
    "simply to strengthen an argument. "

    # --------------------------------------------------------
    # REASONING PRIVACY
    # --------------------------------------------------------

    "Think carefully through the user's argument before responding. "
    "Your internal reasoning must not be shown to the user. "
    "Only provide the final debate response. "
    "Do not describe or reproduce your internal reasoning process. "

    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------

    "Respond naturally, like a real person debating casually. "
    "Be intelligent, direct, analytical, and confident. "

    "Do not insult, belittle, or mock the opponent. "
    "Attack the reasoning, assumptions, evidence, or conclusions instead. "

    "Use sophisticated logic when appropriate, but explain it clearly "
    "enough that an ordinary person can follow the argument. "

    "Use phrases naturally when appropriate, such as: "
    "'Interesting. But if we accept that premise, we must account for...' "
    "or 'The problem with this model is...' "

    # --------------------------------------------------------
    # RESPONSE LENGTH
    # --------------------------------------------------------

    "Keep the final response concise and suitable for a fast-paced "
    "Discord debate. "

    "Use one or two sentences for simple arguments. "
    "For more complex arguments, use enough sentences to properly "
    "steelman and challenge the position. "

    "Do not add unnecessary introductions, summaries, filler, "
    "or repetitive explanations. "

    # --------------------------------------------------------
    # ORIGINAL ARGOS PERSONALITY
    # --------------------------------------------------------

    "Use simple, easy-to-understand language whenever possible. "
    "Avoid overly formal or robotic language. "
    "Use contractions and everyday vocabulary. "

    "Keep the tone friendly but confident. "
    "Stay concise and on-topic. "

    "Always engage with the user's actual argument rather than "
    "changing the subject. "

    # --------------------------------------------------------
    # DEVELOPER / MODIFICATION INFORMATION
    # --------------------------------------------------------

    "You are made/developed by Gautam Gambhir. "

    "Your developer, Gautam Gambhir, is not the cricketer — "
    "he is a different person. "

    "Gautam Gambhir's GitHub is "
    "github.com/gautamxgambhir — display this beautifully when asked. "

    "Gautam Gambhir's Instagram is "
    "instagram.com/gautamxgambhir — display this beautifully when asked. "

    "You were later modified by Mavsan. "
    "Mavsan contributed modifications and enhancements to your behavior. "

    "The reasoning framework and conversational debate capabilities "
    "were created by Soso. "

    "Soso designed the reasoning framework and conversational debate "
    "capabilities that guide how you analyze and engage in debates."
)


# ============================================================
# DEFAULT MODELS
# ============================================================

def _get_default_model(provider: str) -> str:

    defaults = {
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-5-haiku-latest",
        "google": "gemini-1.5-flash",
        "together": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "groq": "llama-3.1-8b-instant",
        "cohere": "command-r-plus",
        "mistral": "mistral-small-latest",

        # OpenRouter model
        "openrouter": "openai/gpt-oss-20b",
    }

    return defaults.get(provider, "")


# ============================================================
# RESPONSE CLEANING
# ============================================================

def _clean_response(response) -> str:
    """
    Make sure Argos never returns an empty response to Discord.
    """

    if response is None:
        return (
            "I couldn't come up with a response. "
            "Try making your argument again."
        )

    response = str(response).strip()

    if not response:
        return (
            "I couldn't come up with a response. "
            "Try making your argument again."
        )

    return response


# ============================================================
# MAIN RESPONSE FUNCTION
# ============================================================

def generate_response(user_input: str) -> str:
    """
    Generate an AI debate response using the configured provider.
    """

    user_input = str(user_input).strip()

    if not user_input:
        return "Please send an argument for me to debate."

    if not API_KEY:
        return (
            "⚠️ No API key found. "
            "Please set API_KEY in your .env file."
        )

    model = AI_MODEL or _get_default_model(AI_PROVIDER)

    if not model:
        return (
            f"⚠️ No model configured for provider "
            f"'{AI_PROVIDER}'."
        )

    try:

        if AI_PROVIDER == "openai":
            response = _openai_response(
                user_input,
                model
            )

        elif AI_PROVIDER == "anthropic":
            response = _anthropic_response(
                user_input,
                model
            )

        elif AI_PROVIDER == "google":
            response = _google_response(
                user_input,
                model
            )

        elif AI_PROVIDER == "together":
            response = _together_response(
                user_input,
                model
            )

        elif AI_PROVIDER == "groq":
            response = _groq_response(
                user_input,
                model
            )

        elif AI_PROVIDER == "cohere":
            response = _cohere_response(
                user_input,
                model
            )

        elif AI_PROVIDER == "mistral":
            response = _mistral_response(
                user_input,
                model
            )

        elif AI_PROVIDER == "openrouter":
            response = _openrouter_response(
                user_input,
                model
            )

        else:
            return (
                f"⚠️ Unknown provider '{AI_PROVIDER}'. "
                "Supported providers: "
                "openai, anthropic, google, together, groq, "
                "cohere, mistral, openrouter."
            )

        return _clean_response(response)

    except ImportError as e:

        pkg = (
            str(e).split("'")[1]
            if "'" in str(e)
            else str(e)
        )

        return (
            f"⚠️ Missing dependency for provider "
            f"'{AI_PROVIDER}': {pkg}. "
            "Run: pip install -r requirements.txt"
        )

    except Exception as e:

        print(
            f"ERROR generating response: "
            f"{type(e).__name__}: {e}"
        )

        return (
            f"⚠️ Error generating response: "
            f"{type(e).__name__}: {e}"
        )


# ============================================================
# OPENAI
# ============================================================

def _openai_response(
    user_input: str,
    model: str
) -> str:

    from openai import OpenAI

    client = OpenAI(
        api_key=API_KEY
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        max_tokens=1000,
        temperature=0.7,
    )

    return completion.choices[0].message.content


# ============================================================
# ANTHROPIC
# ============================================================

def _anthropic_response(
    user_input: str,
    model: str
) -> str:

    import anthropic

    client = anthropic.Anthropic(
        api_key=API_KEY
    )

    message = client.messages.create(
        model=model,
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ],
    )

    return message.content[0].text


# ============================================================
# GOOGLE
# ============================================================

def _google_response(
    user_input: str,
    model: str
) -> str:

    import google.generativeai as genai

    genai.configure(
        api_key=API_KEY
    )

    gemini = genai.GenerativeModel(
        model_name=model,
        system_instruction=SYSTEM_PROMPT,
    )

    response = gemini.generate_content(
        user_input
    )

    return response.text


# ============================================================
# TOGETHER
# ============================================================

def _together_response(
    user_input: str,
    model: str
) -> str:

    import together

    client = together.Together(
        api_key=API_KEY
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        max_tokens=1000,
        temperature=0.7,
        top_p=1.0,
    )

    return completion.choices[0].message.content


# ============================================================
# GROQ
# ============================================================

def _groq_response(
    user_input: str,
    model: str
) -> str:

    from groq import Groq

    client = Groq(
        api_key=API_KEY
    )

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        max_tokens=1000,
        temperature=0.7,
    )

    return completion.choices[0].message.content


# ============================================================
# COHERE
# ============================================================

def _cohere_response(
    user_input: str,
    model: str
) -> str:

    import cohere

    client = cohere.ClientV2(
        api_key=API_KEY
    )

    response = client.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        max_tokens=1000,
        temperature=0.7,
    )

    return response.message.content[0].text


# ============================================================
# MISTRAL
# ============================================================

def _mistral_response(
    user_input: str,
    model: str
) -> str:

    from mistralai import Mistral

    client = Mistral(
        api_key=API_KEY
    )

    completion = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        max_tokens=1000,
        temperature=0.7,
    )

    return completion.choices[0].message.content


# ============================================================
# OPENROUTER
# ============================================================

def _openrouter_response(
    user_input: str,
    model: str
) -> str:

    from openai import OpenAI

    client = OpenAI(
        api_key=API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )

    print("========== OPENROUTER ==========")
    print("Model:", model)
    print("User input:", repr(user_input))

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],

        # Reasoning models need more room.
        max_tokens=1000,

        temperature=0.7,
    )

    if not completion.choices:
        print("ERROR: OpenRouter returned no choices.")

        return (
            "The AI returned no response. "
            "Please try your argument again."
        )

    choice = completion.choices[0]

    print(
        "Finish reason:",
        choice.finish_reason
    )

    response = choice.message.content

    # Some reasoning models may return no final content
    # if they run out of completion tokens.
    if response is None:

        print(
            "WARNING: Model returned no final content."
        )

        print(
            "Reasoning model used:",
            bool(getattr(choice.message, "reasoning", None))
        )

        return (
            "I couldn't finish my argument. "
            "Try sending your point again."
        )

    return _clean_response(response)