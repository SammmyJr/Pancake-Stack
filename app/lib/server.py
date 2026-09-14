import asyncio
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from .model import chat

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(intents=intents, command_prefix="!")


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):
    # ignore the bot's own messages
    if message.author == bot.user:
        return

    # message.guild is None for DMs
    if message.guild is None:
        response = await asyncio.to_thread(chat, message.content)
        if response:
            await message.channel.send(response)


@bot.tree.command(name="ping", description="Responds with a pong!")
async def ping(interaction: discord.Interaction):
    # Always respond using interaction.response.send_message
    await interaction.response.send_message("Pong! 🏓")


def run():
    if token:
        bot.run(token)
    else:
        print("Missing 'DISCORD_TOKEN' in .env!")
