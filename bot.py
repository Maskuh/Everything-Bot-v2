# bot.py
#Import list
import os
import discord
import time
import datetime
import asyncio
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
#________________________________________________
#File Configs
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#TOKEN = os.getenv('Testing_bot')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, owner_id=os.getenv("Owner"), case_insensitive=True)
bot.help_command = None
#______________________________________________________________________________________________

@bot.command()
async def load(ctx, extension):
  if ctx.author.id != int(os.getenv("Owner")):
    await ctx.channel.send(f"You can't load a cog only the bot owner can!")
  else:
    try:
      await bot.load_extension(f'cogs.{extension}')
      await ctx.channel.send("Cog loaded!")
      print(f"{extension} Cog was loaded")
    except Exception as e:
            await ctx.channel.send(f"{e}")



@bot.command()
async def reload(ctx, extension):
  if ctx.author.id != int(os.getenv("Owner")):
    await ctx.channel.send(f"You can't reload a cog only the bot owner can!")
  else:
    try:
      await bot.reload_extension(f'cogs.{extension}')
      await ctx.channel.send("Cog reloaded!")
      print(f"{extension} was reloaded")
    except Exception as e:
            await ctx.channel.send(f"{e}")

@bot.command()
async def unload(ctx, extension):
  if ctx.author.id != int(os.getenv("Owner")):
    await ctx.channel.send(f"You can't unload a cog only the bot owner can!")
  else:
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.channel.send("Cog unloaded!")
    print(f"{extension} was unloaded")


@bot.event
async def on_ready():
  await bot.load_extension("cogs.fun")
  await bot.load_extension("cogs.commands")
  await bot.load_extension("cogs.leave")
  await bot.load_extension("cogs.welcome")
  await bot.load_extension("cogs.join")
  await bot.load_extension("cogs.Kingdom")
  await bot.load_extension("cogs.moderation")
  await bot.load_extension("cogs.HRS")
  await bot.tree.sync()
  await bot.change_presence(status= discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name='How to add more commands to my library of commands!'))
  for guild in bot.guilds:
    print(guild.name)
    print(guild.me.guild_permissions)
    print(f'{bot.user} is connected to the following guild:\n {guild.name}(id: {guild.id}) \n')
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
  
#runs the bot
bot.run(TOKEN)