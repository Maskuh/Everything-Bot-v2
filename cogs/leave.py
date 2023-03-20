import os
import discord
import time
import datetime
import asyncio
import pymongo
from discord.ext import commands
from discord import Webhook, app_commands
from pymongo import MongoClient
import aiohttp
cluster = MongoClient(os.getenv("Mongo"))
db = cluster["discord"]
collection = db["Leaver"]
class leave(commands.GroupCog):
    def __init__(self, client):
        self.client = client
    
#leave commands

    @app_commands.command(description="Sets up a leave message")
    @app_commands.describe(channel="The channel you want your leave message in")
    @app_commands.describe(message="The message you want the bot to send on someone leavign")
    async def enable(self,interaction: discord.Interaction,channel : discord.TextChannel,message: str):
        result = collection.find_one({"_id": interaction.guild.id})
        if result :
            collection.update_one({"_id": interaction.guild.id}, {"$set":{f"{interaction.guild.id}": [channel.id,message]}})
            await interaction.response.send_message("leave message updated!")
            return
        else:
            collection.insert_one({"_id": interaction.guild.id, f"{interaction.guild.id}": [channel.id, message]})
            await interaction.response.send_message("leave message enabled!")
        

    @app_commands.command(description="Removes leave message from database")
    async def disable(self,interaction: discord.Interaction):
        results = collection.find({"_id": interaction.guild.id})
        for result in results:
           if result["_id"] == interaction.guild.id:
                collection.delete_one({"_id": interaction.guild.id})
                await interaction.response.send_message("I have removed the guild from the database!")
           else:
                await interaction.response.send_message("There is no leave message in the database!")



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
