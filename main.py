import os
import discord
from discord.ext import commands
from dotenv import load_dotenv 
from leveling_sys import Adding_Xp

# Token stuff
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("No Token Found.")


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="/", intents=intents)

@client.event
async def on_ready():
    print("Ready")

@client.command()
async def test(ctx):
    await ctx.send("Test")

@client.event
async def on_message(message):
    # ignore bots own messages
    if message.author == client.user:
        return

    # fetch the user's id 
    UserId = message.author.id
    Adding_Xp(UserId, 10)

client.run(TOKEN)