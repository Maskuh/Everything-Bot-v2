import os
import discord
import time
import datetime
import asyncio
from discord.ext import commands

class Events(commands.Cog):

    def __init__(self,client):
        self.client = client
        async def cog_load(self):
            await self.client.change_presence(status= discord.Status.online, activity=discord.Game(f'%help Learning how to add more commands to my library of commands!'))
            for guild in self.client.guilds:
                print(guild.name)
                print(guild.me.guild_permissions)
                print(
                f'{self.client.user} is connected to the following guild:\n'
                f'{guild.name}(id: {guild.id}) \n')
    
                members = '\n - '.join([member.name for member in guild.members])
                print(f'Guild Members:\n - {members}')
            




async def setup(client):
    await client.add_cog(Events(client))      
