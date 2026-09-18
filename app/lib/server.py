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


# runs on client connect
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


# runs on message recieved
@bot.event
async def on_message(message):
    # ignore the bot's own messages
    if message.author == bot.user:
        return

    # message.guild is None for DMs
    if message.guild is None:
        statusMessage = await message.channel.send("⏳ Thinking...")

        # get response from model
        response = await chat(message.content, statusMessage)
        if response:
            # delete status and tool call messages, send the model's response
            await statusMessage.delete()
            await message.channel.send(response)


def run():
    if token:
        bot.run(token)
    else:
        print("Missing 'DISCORD_TOKEN' in .env!")
