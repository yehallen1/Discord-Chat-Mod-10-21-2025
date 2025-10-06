import os
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from dotenv import load_dotenv 
from leveling_sys import Adding_Xp

# Token stuff
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("No Token Found.")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="/", intents=intents)

@client.event
async def on_ready():
    print("Ready")

@client.command()
async def test(ctx):
    await ctx.send("Test")



# used to detect messages for adding XP to data base
@client.event
async def on_message(message):
    # ignore the bots own messages
    if message.author == client.user:
        return
    
    # ignore '/' commands
    if message.content.startswith("/"):
        return

    # fetch the user's id 
    UserId = message.author.id
    Adding_Xp(UserId, 10)



# Detects when someone joins the server.
# Kevin this might be useful to keep metrics on when someone joins the server. 
@client.event
async def on_member_join(member):
    await member.send()

@client.event
async def on_member_remove(member):
    await member.send()

# For playing audio in voice calls. 

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member} has been kicked.')
    
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Error: You do not have permission to kick people.")

@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned.')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Error: You do not have permission to ban people.")

@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        # source = FFmpegPCMAudio( FILE NAME HERE )
        # player = voice.play(source)


@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("left voice channel")
    else:
        await ctx.send("Not in a voice channel.")

client.run(TOKEN)