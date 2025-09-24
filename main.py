import os
import discord
from discord.ext import commands
from dotenv import load_dotenv 

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

client.run(TOKEN)