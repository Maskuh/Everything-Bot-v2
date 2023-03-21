import os
import discord
import time
import datetime
import asyncio
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

class Moderation(commands.GroupCog):

    def __init__(self, client):
        self.client = client
        load_dotenv()

    @app_commands.command(description='purge Amount of messages')
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, limit: int):
            if not limit:
                purge_failed = discord.Embed(title='Purge [%Purge]', description=f'Failed to Purge {limit} messages. \n Command executed by {interaction.user}.', color=discord.Colour.random())
                purge_failed.set_footer(text=str(datetime.datetime.now()))
                return await interaction.response.send_message(embed=purge_failed)
            await asyncio.sleep(1)
            await interaction.channel.purge(limit=limit)
            purge_embed = discord.Embed(title='Purge [%Purge]', description=f'Successfully Purged {limit} messages. \n Command executed by {interaction.user}.', color=discord.Colour.random())
            purge_embed.set_footer(text=str(datetime.datetime.now()))
            await interaction.response.send_message(embed=purge_embed)
    #@purge.error
    #async def sendback(self, interaction: discord.Interaction, error: commands.CommandError):
     #   if isinstance(error, commands.MissingPermissions):  
      #    await interaction.response.send_message(f"{interaction.user.mention}You do not have permissions to do this command.")


    
async def setup(client):
     await client.add_cog(Moderation(client)) 