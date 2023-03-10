import os
import discord
import time
import datetime
import asyncio
from discord.ext import commands, tasks


class Basic_commands(commands.Cog):

    def __init__(self, client):
        self.client = client

# Ping command
    @commands.command(name='Ping')
    async def Ping(self, ctx):
        await ctx.channel.send(f"**Pong!** That took {int(self.client.latency*1000)} ms!")
#Invite command
    @commands.command(name='Invite')
    async def Invite(self, ctx):
        embed=discord.Embed(title='Invite Links!', description=f"[Invite(recommended)](https://discord.com/api/oauth2/authorize?client_id=902249858281394237&permissions=274877999168&scope=bot) \n [Invite(admin)](https://discord.com/api/oauth2/authorize?client_id=902249858281394237&permissions=8&scope=bot)", color=0x2ecc71)
        await ctx.channel.send(embed=embed)

    @commands.command(name='Leave')
    @commands.check_any(commands.is_owner(), commands.has_guild_permissions(manage_guild=True))
    async def Leave(self,ctx):
        await ctx.channel.send("Very well, idk why you would want me to leave but ok bye")
        await asyncio.sleep(1)
        await ctx.guild.leave()     
    #@Leave.error
    async def pushback(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
          await ctx.send(f"{ctx.author.mention}You do not have permissions to do this command.")


    @commands.command(name='Support')
    async def Support(self,ctx):
        embed=discord.Embed(title='Support link', description="[Invite] (https://discord.gg/3setXsQJZu)", color=0x2ecc71)
        await ctx.channel.send(embed=embed)

    
    @commands.command()
    async def stats(self, ctx):
        channel = self.client.get_channel(957089374066077696)
        members = 0
        for guild in self.client.guilds:
            members += guild.member_count - 1
                
        embed=discord.Embed(title="Bot Stats")
        embed.set_author(name="Made by Maskuh#3454")
        embed.add_field(name="Guilds", value=f"```{len(self.client.guilds)}```", inline=True) 
        embed.add_field(name="Users", value=f"```{members}```", inline=True)
        await channel.send(embed=embed)
    
    @commands.command()
    async def permissions(self, ctx, channel):
        em = discord.Embed(title=f'Testing', description=f"I am testing if i have permissions in this channel!")
        channel = channel = await self.client.fetch_channel(channel)
        try:
            await channel.send(embed=em, delete_after=2)
            await ctx.channel.send("I was able to send the embed and delete it after!")

        except Exception as e:
            await ctx.channel.send(f"{e}")



async def setup(client):
     await client.add_cog(Basic_commands(client)) 
