import os
import discord
import flask_app
import leveling_sys as lvl
from threading import Thread
from flask import Flask, request, jsonify, render_template
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from dotenv import load_dotenv 


# Token stuff
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("No Token Found.")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="/", intents=intents)


# initialize database on startup
@client.event
async def on_ready():
    await lvl.init_db()
    print("Ready")

    # Multithreading for Flask
    flask_thread = Thread(target=flask_app.run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    #flask API stuff
    file = open('guilds.txt', 'w+')
    guilds = client.guilds
    
    for guild in guilds:
        file.write(f'{guild.id}:{guild.name}\n')
    file.close()


@client.command()
async def test(ctx):
    await ctx.send("Test")

# ========================================
# Leveling system
# =========================================

# /level command to print XP and Level
@client.command()
async def level(ctx):
    user_id = str(ctx.author.id)
    xp, level = await lvl.print_level(user_id)
    await ctx.send(f"Hello, {ctx.author.name}!\nYour current Level is {level} and Xp is at {xp}")


# used to detect messages for adding XP to data base
@client.event
async def on_message(message):
    # ignore the bots own messages
    if message.author == client.user:
        return
    
    # ignore / commands otherwise gives XP still
    if message.content.startswith("/"):
        await client.process_commands(message)
        return

    # fetch the user's id 
    UserId = str(message.author.id)
    await lvl.add_xp(UserId, 10)

    # Allow other bot commands (like /level or /test) to still work after this event
    await client.process_commands(message)


# Detects when someone joins the server.
# Kevin this might be useful to keep metrics on when someone joins the server. 
@client.event
async def on_member_join(member):
    # add user_id to the datbase on join
    user_id = str(member.id)
    await lvl.auto_user(user_id)
    await member.send()

@client.event
async def on_member_remove(member):
    await member.send()


# ==========================
# Music Playback
# ==========================

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