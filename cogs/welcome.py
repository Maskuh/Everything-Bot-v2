import os
import discord
import time
import datetime
import asyncio
import pymongo
from discord.ext import commands
from dotenv import load_dotenv
from discord import Webhook, app_commands
from pymongo import MongoClient
import aiohttp
import motor.motor_asyncio
cluster = MongoClient(os.getenv("Mongo"))
db = cluster["discord"]
collection = db["welcomer"]
class Welcome(commands.GroupCog):
    def __init__(self, client):
        self.client = client
        load_dotenv()
    
#welcome commands

    @app_commands.command(description="Enable a Welcome message for your server")
    @app_commands.describe(channel="The channel for the welcome message")
    @app_commands.describe(message="The message you want the bot to send")
    async def enable(self,interaction: discord.Interaction,channel : discord.TextChannel, message: str):
        result = collection.find_one({"_id": interaction.guild.id})
        if result :
            collection.update_one({"_id": interaction.guild.id}, {"$set":{f"{interaction.guild.id}": [channel.id,message]}})
            await interaction.response.send_message("welcome message updated!")
            return
        else:
            collection.insert_one({"_id": interaction.guild.id, f"{interaction.guild.id}": [channel.id, message]})
            await interaction.response.send_message("Welcome message enabled!")
        

    @app_commands.command(description="Removes your welcome message from the database")
    async def disable(self,interaction: discord.Interaction):
        results = collection.find({"_id": interaction.guild.id})
        for result in results:
           if result["_id"] == interaction.guild.id:
                collection.delete_one({"_id": interaction.guild.id})
                await interaction.response.send_message("I have removed the guild from the database!")
           else:
                await interaction.response.send_message("There is no welcome message in the database!")



    @commands.Cog.listener()
    async def on_member_join(self,member : discord.member):
        guild_id = member.guild.id
        result = collection.find_one({"_id": member.guild.id})
        if result is None: return

        else:
            channel_id = result[f'{member.guild.id}'][0]
            channel = self.client.get_channel(channel_id)
            welcome_message = result[f'{member.guild.id}'][1] 
            first_message = welcome_message
            second_message = first_message.replace("{member.mention}",f"{member.mention}")
            third_message = second_message.replace("{member}",f"{member}")
            final_message = third_message.replace("{member.guild}",f"{member.guild}")
            await channel.send(f"{final_message}")


 




async def setup(client):
    await client.add_cog(Welcome(client))
