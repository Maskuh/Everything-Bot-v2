import os
import discord
import time
import datetime
import asyncio
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv

class hrs(commands.GroupCog):
    def __init__(self, client):
        self.client = client
        load_dotenv()
    
    @app_commands.command(description="Sends Message of the next run time")
    @app_commands.describe(channel="The Channel to send in.")
    @app_commands.rename(fr = "from")
    @app_commands.describe(fr="Where you are going from.")
    @app_commands.describe(to="Where your going to.")
    @app_commands.describe(boarding=" When You're boarding, In Time Stamp Format")
    @app_commands.describe(departure="What Time You're Departing, In Time Stamp Format")
    @app_commands.describe(arrival="When You're Planing To Arrive At Your destination, In Time Stamp Format")
    @app_commands.describe(loco="The locomotive used")
    @app_commands.describe(server="The server used for the run")
    async def runtime(self, interaction: discord.Interaction, channel: discord.TextChannel, fr:str, to:str,boarding:str, departure:str, arrival:str, loco:str, server:str):
        if interaction.guild.id != int(os.getenv("Guild")): return
        try:
            chanel = self.client.get_channel(channel.id)
            em = discord.Embed(title=f"Horizon Railway Service: Running At {boarding}", description=f"The Train is running from {fr} to {to} \n Boarding time : {boarding} \n Departure time: {departure} \n Arrival time: {arrival} \n First class tickets: 30cr (While Supplies last) \n Second class tickets: 20cr \n The Locomotive Being Used Is The: {loco} \n The Server This Will Be Hosted On Is {server} **(Subject to change last minute!)** \n Thank you for choosing Horizon Railway Service!")
            await chanel.send(embed=em)
            await interaction.response.send_message(f"I have sent the runtime to channel <#{channel.id}>")
        except:
            await interaction.response.send_message("I have failed to send the Embed containing that information please check my permissions!")
        
async def setup(client):
     await client.add_cog(hrs(client)) 