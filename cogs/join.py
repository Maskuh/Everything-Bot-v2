import os
import discord
import time
import datetime
import asyncio
import pymongo
from discord.ext import commands
from discord import Webhook
from dotenv import load_dotenv
class join(commands.Cog):
    def __init__(self, client):
        self.client = client
        load_dotenv()

    @commands.Cog.listener()
    async def on_member_join(self, member : discord.member):
        if member.bot: return
        if member.guild.id == 902404450432483378:
            channel = self.client.get_channel(904216443166543964)
            em = discord.Embed(title=f'Welcome {member}', description=f"Hey, {member.mention} Welcome to {member.guild}! \n \n Please read the rules in <#925976154890993734> \n \n You can get support for my bot in <#904216450707881994> \n \n Please enjoy your stay!", timestamp=datetime.datetime.now())
            em.set_thumbnail(url=member.avatar_url)
            await channel.send(embed=em)
            try:
                role = member.guild.get_role(904216437399355402)
                await member.add_roles(role)
            except Exception as e: 
                channe = self.client.get_channel(904216460640010251)
                await channe.send(f"{e}")

async def setup(client):
    await client.add_cog(join(client))