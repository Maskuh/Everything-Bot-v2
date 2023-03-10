# bot.py
#Import list
import os
import discord
import time
import datetime
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://maskuh:Pusd4996@cluster0.qnihg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["prefix"]
#________________________________________________
#File Configs
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='%', intents=intents, owner_id=786788350160797706, case_insensitive=True)
bot.help_command = commands.MinimalHelpCommand()
#______________________________________________________________________________________________

@bot.command()
async def load(ctx, extension):
  if ctx.author.id != 786788350160797706:
    await ctx.channel.send(f"You can't load a cog only the bot owner can!")
  else:
    try:
      await bot.load_extension(f'cogs.{extension}')
      await ctx.channel.send("Cog loaded!")
    except Exception as e:
            await ctx.channel.send(f"{e}")



@bot.command()
async def reload(ctx, extension):
  if ctx.author.id != 786788350160797706:
    await ctx.channel.send(f"You can't reload a cog only the bot owner can!")
  else:
    try:
      await bot.reload_extension(f'cogs.{extension}')
      await ctx.channel.send("Cog reloaded!")
    except Exception as e:
            await ctx.channel.send(f"{e}")

@bot.command()
async def unload(ctx, extension):
  if ctx.author.id != 786788350160797706:
    await ctx.channel.send(f"You can't unload a cog only the bot owner can!")
  else:
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.channel.send("Cog unloaded!")


@bot.event
async def on_ready():
  await bot.load_extension("cogs.fun")
  await bot.load_extension("cogs.events")
  await bot.load_extension("cogs.commands")
  await bot.load_extension("cogs.leave")
  await bot.load_extension("cogs.welcome")
  await bot.load_extension("cogs.join")
  await bot.load_extension("cogs.Kingdom")
  await bot.load_extension("cogs.moderation")

bot.run(TOKEN)