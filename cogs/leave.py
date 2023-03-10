import os
import discord
import time
import datetime
import asyncio
import pymongo
from discord.ext import commands
from discord import Webhook
from pymongo import MongoClient
import aiohttp
cluster = MongoClient("mongodb+srv://maskuh:Pusd4996@cluster0.qnihg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["Leaver"]
class leave(commands.Cog):
    def __init__(self, client):
        self.client = client
    
#welcome commands

    @commands.command(name='lenable')
    async def lenable(self,ctx,channel : discord.TextChannel,*,arg):
        result = collection.find_one({"_id": ctx.guild.id})
        message = arg
        if result :
            collection.update_one({"_id": ctx.guild.id}, {"$set":{f"{ctx.guild.id}": [channel.id,message]}})
            await ctx.channel.send("leave message updated!")
            return
        else:
            collection.insert_one({"_id": ctx.guild.id, f"{ctx.guild.id}": [channel.id, message]})
            await ctx.channel.send("leave message enabled!")
        

    @commands.command(name='ldisable')
    async def ldisable(self,ctx):
        results = collection.find({"_id": ctx.guild.id})
        for result in results:
           if result["_id"] == ctx.guild.id:
                collection.delete_one({"_id": ctx.guild.id})
                await ctx.channel.send("I have removed the guild from the database!")
           else:
                await ctx.channel.send("There is no leave message in the database!")



    @commands.Cog.listener()
    async def on_member_remove(self,member : discord.member):
        guild_id = member.guild.id
        result = collection.find_one({"_id": member.guild.id})
        if result is None: return

        else:
            channel_id = result[f'{member.guild.id}'][0]
            channel = self.client.get_channel(channel_id)
            leave_message = result[f'{member.guild.id}'][1] 
            first_message = leave_message
            second_message = first_message.replace("{member.mention}",f"{member.mention}")
            third_message = second_message.replace("{member}",f"{member}")
            final_message = third_message.replace("{member.guild}",f"{member.guild}")
            await channel.send(f"{final_message}")





async def setup(client):
    await client.add_cog(leave(client))
