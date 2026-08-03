<div align="center">
  <img src="https://i.ibb.co/ZpLTY3CS/argos.png" alt="Argos Logo"><br>
</div>

-----------------

# Argos: AI-Powered Debate Bot for Telegram & Discord

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-red)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue)
![Discord](https://img.shields.io/badge/Discord-Bot-purple)

## What is Argos?

Argos is an AI-powered **debate bot** for **Telegram & Discord** that challenges users on any topic by taking the opposing stance. Whether you argue **in favor** or **against** a subject, Argos will always take the opposite position, ensuring a balanced and thought-provoking discussion.

## Features

- **Opposing Debate Stance**: If you argue *in favor* of a topic, Argos will argue *against* it, and vice versa.
- **Supports Telegram & Discord**: Available as both a **Telegram bot** and a **Discord bot**.
- **Bring Your Own API Key**: Works with any major AI provider — you're never locked in to one service.
- **Multi-Provider Support**: Supports OpenAI, Anthropic, Google Gemini, Together AI, Groq, Cohere, Mistral, and OpenRouter out of the box.
- **Fast & Dynamic**: Provides quick responses to keep the debate engaging.
- **Customizable Prefix for Discord**: Uses `!` as the default prefix for Discord commands.

## Supported AI Providers

| `AI_PROVIDER` value | Service | Get API Key |
|---|---|---|
| `openai` | OpenAI (GPT-4o, etc.) | [platform.openai.com](https://platform.openai.com/api-keys) |
| `anthropic` | Anthropic (Claude) | [console.anthropic.com](https://console.anthropic.com/) |
| `google` | Google Gemini | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| `together` | Together AI | [api.together.ai](https://api.together.ai/) |
| `groq` | Groq (fast inference) | [console.groq.com](https://console.groq.com/keys) |
| `cohere` | Cohere | [dashboard.cohere.com](https://dashboard.cohere.com/api-keys) |
| `mistral` | Mistral AI | [console.mistral.ai](https://console.mistral.ai/) |
| `openrouter` | OpenRouter (unified gateway) | [openrouter.ai](https://openrouter.ai/keys) |

## Bot Descriptions

### **Discord Bot**
Use commands like `!start`, `!stop`, and `!dm` to begin or end a debate session.

### **Telegram Bot**
Start with `/start`, chat in DM with `/dm`, and end with `/stop`.

## Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/gautamxgambhir/Argos.git
cd Argos
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> You can also install only the SDK for your chosen provider instead of all of them. See the comments in `requirements.txt`.

### 3. Configure your `.env` file

Copy the example file and fill in your values:
```bash
cp .env.example .env
```

Then edit `.env`:
```env
# Choose your AI provider
AI_PROVIDER=openai

# Your API key for that provider
API_KEY=your_api_key_here

# (Optional) Override the default model
AI_MODEL=

# Bot tokens
TELEGRAM_TOKEN=your_telegram_bot_token
DISCORD_TOKEN=your_discord_bot_token
```

#### Default models per provider
If you leave `AI_MODEL` blank, Argos uses a sensible default for your chosen provider:

| Provider | Default model |
|---|---|
| openai | `gpt-4o-mini` |
| anthropic | `claude-3-5-haiku-latest` |
| google | `gemini-1.5-flash` |
| together | `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` |
| groq | `llama-3.1-8b-instant` |
| cohere | `command-r-plus` |
| mistral | `mistral-small-latest` |
| openrouter | `openai/gpt-4o-mini` |

### 4. Set up bot tokens
- **Telegram**: Create a bot via [BotFather](https://core.telegram.org/bots#botfather) and paste the token as `TELEGRAM_TOKEN`.
- **Discord**: Create an application at the [Discord Developer Portal](https://discord.com/developers/applications), add a bot, and paste the token as `DISCORD_TOKEN`.

### 5. Run the bot
```bash
# Discord
python discordbot.py

# Telegram
python telegrambot.py
```

## Discord Bot Usage

- **Prefix**: `!`
- **Commands**:
  - `!start` → Start a debate session in the current channel.
  - `!stop` → End the active debate session.
  - `!dm` → Start a debate session in your DMs.
- Just type any statement after `!start` and Argos will counter it.

## Telegram Bot Usage

- **Commands**:
  - `/start` → Start a debate session.
  - `/stop` → End the debate session.
  - `/restart` → Restart the current session.
  - `/dm` → Start a debate in DM.
- Just type any statement after `/start` and Argos will counter it.

## Dependencies

- [**discord.py**](https://discordpy.readthedocs.io/en/stable/) — Discord bot framework.
- [**python-telegram-bot**](https://python-telegram-bot.readthedocs.io/) — Telegram bot framework.
- [**python-dotenv**](https://pypi.org/project/python-dotenv/) — Loads `.env` variables.
- One of: **openai**, **anthropic**, **google-generativeai**, **together**, **groq**, **cohere**, **mistralai** — depending on your chosen provider.

## Contributing

Contributions are welcome!
- Fork the repo.
- Create a new branch: `git checkout -b feature-branch`
- Commit your changes: `git commit -m "Added new feature"`
- Push to the branch: `git push origin feature-branch`
- Open a pull request.

## License

This project is licensed under the **MIT License**.

## Contact

- **GitHub**: [@gautamxgambhir](https://github.com/gautamxgambhir)
- **Email**: ggambhir1919@gmail.com
- **Instagram**: [gautamxgambhir](https://www.instagram.com/gautamxgambhir)
- **Twitter**: [gautamxgambhir](https://www.twitter.com/gautamxgambhir)
