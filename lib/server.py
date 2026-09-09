import os
from dotenv import load_dotenv
import discord
from .model import chat

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    # ignore the bot's own messages
    if message.author == client.user:
        return

    # message.guild is None for DMs
    if message.guild is None:
        response = chat(message.content)
        if response:
            await message.channel.send(response)


def run():
    if token:
        client.run(token)
    else:
        print("Missing 'DISCORD_TOKEN' in .env!")
