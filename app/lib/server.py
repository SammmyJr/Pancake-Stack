import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from .model import chat

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
owner_id = os.getenv("USER_ID")

if owner_id:
    owner_id = int(owner_id)

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(intents=intents, command_prefix="!")

keyword = "kupo"


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
        await respond(message)
    else:
        # check if the author is the bot owner, don't want to reply to other people!
        if message.author.id == owner_id:
            # check if the author has invoked the model with a keywords
            if message.content.lower().startswith(keyword):
                await respond(message)


async def respond(message: discord.Message):
    statusMessage = await message.reply("⏳ Thinking...", mention_author=False)

    # get response from model
    response = await chat(message.content, statusMessage)
    if response:
        # delete status and tool call messages, send the model's response
        await statusMessage.delete()
        await message.reply(response, mention_author=True)


def run():
    if token and owner_id:
        bot.run(token)
    else:
        print("Missing 'DISCORD_TOKEN' or 'USER_ID' in .env!")
