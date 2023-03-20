import os
import discord
import time
import datetime
import asyncio
from discord.ext import commands, tasks
from discord import app_commands


class commands(commands.GroupCog):

    def __init__(self, client):
        self.client = client

# Ping command
    @app_commands.command(description="check the ping of the bot!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"**Pong!** That took {int(self.client.latency*1000)} ms!")
#Invite command
    @app_commands.command(description="Sends Invite link to you to invite the bot")
    async def invite(self, interaction: discord.Interaction):
        embed=discord.Embed(title='Invite Links!', description=f"[Invite(recommended)](https://discord.com/api/oauth2/authorize?client_id=902249858281394237&permissions=274877999168&scope=bot) \n [Invite(admin)](https://discord.com/api/oauth2/authorize?client_id=902249858281394237&permissions=8&scope=bot)", color=0x2ecc71)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Makes the bot leave the guild")
    @commands.check_any(commands.is_owner(), commands.has_guild_permissions(manage_guild=True))
    async def leave(self, interaction: discord.Interaction):
        await interaction.response.send_message("Very well, idk why you would want me to leave but ok bye")
        await asyncio.sleep(1)
        await interaction.guild.leave()     



    @app_commands.command(description="Sends link to the support server")
    async def support(self,interaction: discord.Interaction):
        embed=discord.Embed(title='Support link', description="[Invite] (https://discord.gg/3setXsQJZu)", color=0x2ecc71)
        await interaction.response.send_message(embed=embed)

    
    @app_commands.command(description="Tells you stats of the bot")
    async def stats(self, interaction: discord.Interaction):
        members = 0
        for guild in self.client.guilds:
            members += guild.member_count - 1
                
        embed=discord.Embed(title="Bot Stats")
        embed.set_author(name="Made by Maskuh#3454")
        embed.add_field(name="Guilds", value=f"```{len(self.client.guilds)}```", inline=True) 
        embed.add_field(name="Users", value=f"```{members}```", inline=True)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(description="Checks a Channel for bot writing permissions")
    @app_commands.describe(channel="The Channel to check permissions in")
    async def permissions(self, interaction: discord.Interaction, channel: discord.TextChannel):
        em = discord.Embed(title=f'Testing', description=f"I am testing if i have permissions in this channel!")
        channel  = await self.client.fetch_channel(channel.id)
        try:
            await channel.send(embed=em, delete_after=2)
            await interaction.response.send_message("I was able to send the embed and delete it after!")

        except Exception as e:
            await interaction.response.send_message(f"{e}")



async def setup(client):
     await client.add_cog(commands(client)) 
