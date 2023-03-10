import os
import discord
import time
import datetime
import asyncio
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='Purge')
    @commands.has_permissions(manage_messages=True)
    async def Purge(self, ctx, limit: int = None):
            if not limit:
                purge_failed = discord.Embed(title='Purge [%Purge]', description=f'Failed to Purge {limit} messages. \n Command executed by {ctx.author}.', color=discord.Colour.random())
                purge_failed.set_footer(text=str(datetime.datetime.now()))
                return await ctx.send(embed=purge_failed)
            await ctx.message.delete()
            await asyncio.sleep(1)
            await ctx.channel.purge(limit=limit)
            purge_embed = discord.Embed(title='Purge [%Purge]', description=f'Successfully Purged {limit} messages. \n Command executed by {ctx.author}.', color=discord.Colour.random())
            purge_embed.set_footer(text=str(datetime.datetime.now()))
            await ctx.send(embed=purge_embed)
    #@Purge.error
    async def sendback(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):  
          await ctx.send(f"{ctx.author.mention}You do not have permissions to do this command.")


    
async def setup(client):
     await client.add_cog(Moderation(client)) 