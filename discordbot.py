import os
from datetime import datetime
from threading import Thread
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from flask import Flask
from pytz import timezone

# Custom Module Import
from argos import generate_response

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# ── FLASK HEALTH CHECK WEB SERVER ─────────────────────────────────────────────
app = Flask("")

@app.route("/")
def home():
    return "Argos Bot is alive and well!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# Start the Flask web server thread instantly
Thread(target=run_web_server).start()

# ── DISCORD BOT SETUP ─────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

active_sessions = {}
dm_sessions = {}

def log_interaction(user):
    log_entry = [
        user.name,
        user.id,
        datetime.now(timezone("Asia/Manila")).strftime("%d-%b-%Y %I:%M %p"),
    ]
    print(f"BOT_LOG: {log_entry}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="start")
async def start_debate(ctx):
    channel_id = ctx.channel.id
    if channel_id in active_sessions:
        await ctx.send("A debate session is already active in this channel!")
    else:
        active_sessions[channel_id] = True
        await ctx.send("Debate session started! Type your arguments, and I'll respond. Use `!stop` to end the session.")
        log_interaction(ctx.author)

@bot.command(name="stop")
async def stop_debate(ctx):
    channel_id = ctx.channel.id
    user_id = ctx.author.id

    if channel_id in active_sessions:
        del active_sessions[channel_id]
        await ctx.send("Debate session ended. Thank you for debating with Argos!")
    elif user_id in dm_sessions:
        del dm_sessions[user_id]
        await ctx.author.send("Debate session ended. Thank you for debating with Argos!")
    else:
        await ctx.send("No active debate session in this channel or DM.")
    log_interaction(ctx.author)

@bot.command(name="dm")
async def dm_debate(ctx):
    user_id = ctx.author.id
    if user_id in dm_sessions:
        await ctx.author.send("You already have an active debate session in DM!")
    else:
        dm_sessions[user_id] = True
        await ctx.author.send("Debate session started in DM! Type your arguments, and I'll respond. Use `!stop` to end the session.")
        log_interaction(ctx.author)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    channel_id = message.channel.id
    user_id = message.author.id

    if channel_id in active_sessions:
        try:
            response = generate_response(message.content)
            await message.channel.send(response if response and response.strip() else "I couldn't generate a response. Please try again.")
        except Exception as e:
            await message.channel.send("Sorry, I couldn't process your request. Please try again later.")
            print(f"Error: {type(e).__name__}: {e}")
    elif user_id in dm_sessions and isinstance(message.channel, discord.DMChannel):
        try:
            response = generate_response(message.content)
            await message.channel.send(response if response and response.strip() else "I couldn't generate a response. Please try again.")
        except Exception as e:
            await message.channel.send("Sorry, I couldn't process your request. Please try again later.")
            print(f"Error: {type(e).__name__}: {e}")
    else:
        await bot.process_commands(message)

# ── 💡 NON-BLOCKING ASYNC ENGINE LOOP FOR DEPLOYMENT ──────────────────────────
def run_discord_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start(DISCORD_TOKEN))

if __name__ == "__main__":
    # Boot the bot in its own sub-thread loop so Gunicorn has access to Flask's 'app'
    Thread(target=run_discord_bot).start()