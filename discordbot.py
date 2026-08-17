import asyncio
import os
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv
from pytz import timezone

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "").strip()

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set in the environment."
)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents
)

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
    print(f"✅ SUCCESS: Logged into Discord Gateway as {bot.user}")

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
            from argos import generate_response
            response = generate_response(message.content)
            await message.channel.send(response if response and response.strip() else "I couldn't generate a response. Please try again.")
        except Exception as e:
            await message.channel.send("Sorry, I couldn't process your request. Please try again later.")
            print(f"Error: {type(e).__name__}: {e}")
            
    elif user_id in dm_sessions and isinstance(message.channel, discord.DMChannel):
        try:
            from argos import generate_response
            response = generate_response(message.content)
            await message.channel.send(response if response and response.strip() else "I couldn't generate a response. Please try again.")
        except Exception as e:
            await message.channel.send("Sorry, I couldn't process your request. Please try again later.")
            print(f"Error: {type(e).__name__}: {e}")
    else:
        await bot.process_commands(message)

# ── 3. ASYNC RUN ENGINE ───────────────────────────────────────────────────────
async def main():
    async with bot:
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    # Explicit loop control forces compliance with container threads
    asyncio.run(main())