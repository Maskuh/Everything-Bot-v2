import os
import discord
import time
import datetime
import asyncio
import pymongo
from discord.ext import commands, tasks
from discord import Webhook
class Kingdom(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reaction_roles = 1082486730793426944
        self.channel = self.client.get_channel(1078726726508617859)
    async def cog_load(self):
        print("online!")
        self.vc.cancel()
        self.vc.start()

    

    @commands.Cog.listener()
    async def on_member_join(self, member : discord.member):
        if member.guild.id == 1078694231465541632:
            channel = self.client.get_channel(1078694232111460393)
            em = discord.Embed(title=f'Welcome {member}', description=f"Hey, {member.mention} Welcome to {member.guild}! \n \n Please read the rules in <#1081450694395056168> \n \n  get roles at <#1078726726508617859> Enjoys your vist!", color = discord.Color.from_rgb(4, 3, 97), timestamp=datetime.datetime.now())
            em.set_thumbnail(url=member.avatar)
            await channel.send(embed=em)
            await channel.send(f"{member.mention}",  delete_after=1)
            try:
                if member.bot:
                    ro = member.guild.get_role(1078694231465541633)
                    await member.add_roles(ro)
                    return
                guild = self.client.get_guild(1078694231465541632)
                if len(list(filter(lambda x: not x.bot, guild.members))) <= 500:
                    role = member.guild.get_role(1081510403617599488)
                    await member.add_roles(role)
                rol = member.guild.get_role(1078694231465541634)
                await member.add_roles(rol)
            except Exception as e: 
                channe = self.client.get_channel(1078694232736419877)
                await channe.send(e)

    @commands.Cog.listener()
    async def on_member_remove(self, member : discord.member):
        if member.guild.id == 1078694231465541632:
            channel = self.client.get_channel(1078694232111460394)
            em = discord.Embed(title=f'Goodbye {ctx.author}', description=f"{ctx.author.mention} left {ctx.guild}", color = discord.Color.from_rgb(0, 0, 0), timestamp=datetime.datetime.now())
            em.set_thumbnail(url=ctx.author.avatar)
            await channel.send(embed=em)
    #@commands.command()
    #async def testing(self,ctx):
        #if ctx.guild.id == 1078694231465541632:
        #    channel = self.client.get_channel(1078694232111460393)
         #   em = discord.Embed(title=f'Welcome {ctx.author}', description=f"Hey, {ctx.author.mention} Welcome to {ctx.author.guild}! \n \n Please read the rules in the <#1081450694395056168> channel \n \n  get roles in <#1078726726508617859> Enjoy your vist!", color = discord.Color.from_rgb(4, 3, 97), timestamp=datetime.datetime.now())
          #  em.set_thumbnail(url=ctx.author.avatar)
           # await channel.send(embed=em)
            #await channel.send(f"{ctx.author.mention}",  delete_after=1)
    
    @tasks.loop(minutes=5)
    async def vc(self):
        await self.client.wait_until_ready()
        guild = self.client.get_guild(1078694231465541632)
        hannel = self.client.get_channel(1080366116100132944)
        annel = self.client.get_channel(1080366071229448192)
        channel = self.client.get_channel(1080365938626547772)
        bot_user = len(list(filter(lambda x: x.bot, guild.members)))
        user = len(list(filter(lambda x: not x.bot, guild.members)))
        await channel.edit(name=f"{len(guild.members)} Total Members")
        await hannel.edit(name=f"{user} Humans")
        await annel.edit(name=f"{bot_user} bots")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print("role was triggered")
        guild = self.client.get_guild(payload.guild_id)
        print(f"{payload.emoji.name}")
        if payload.emoji.name == "Giveaways" and payload.message_id == self.reaction_roles:
            print("got here")
            role = discord.utils.get(guild.roles, name="Gw ping")
            if role is not None:
                print("found role")
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                print(f"member: {member}")
                if member is not None:
                    await member.add_roles(role)
                    await self.channel.send(f"{member.mention} I Have added the role Gw ping or you already have it!", delete_after=10)

        elif payload.emoji.name == "Drops" and payload.message_id == self.reaction_roles:
            print("got here")
            role = discord.utils.get(guild.roles, name="Drops ping")
            if role is not None:
                print("found role")
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                print(f"member: {member}")
                if member is not None:
                    await member.add_roles(role)
                    await self.channel.send(f"{member.mention} I Have added the role Drops ping or you already have it!", delete_after=10)

        elif payload.emoji.name == "blueannouncement" and payload.message_id == self.reaction_roles:
            print("got here")
            role = discord.utils.get(guild.roles, name="Announcement ping")
            if role is not None:
                print("found role")
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                print(f"member: {member}")
                if member is not None:
                    await member.add_roles(role)
                    await self.channel.send(f"{member.mention} I Have added the role Dead chat ping or you already have it!", delete_after=10)

        elif payload.emoji.name == "L_chat" and payload.message_id == self.reaction_roles:
            print("got here")
            role = discord.utils.get(guild.roles, name="Dead chat ping")
            if role is not None:
                print("found role")
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                print(f"member: {member}")
                if member is not None:
                    await member.add_roles(role)
                    await self.channel.send(f"{member.metion} I Have added the role Dead Chat Ping or you already have it!", delete_after=10)
        else:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            cha = self.client.get_channel(payload.channel_id)
            message = await cha.fetch_message(self.reaction_roles)
            await self.channel.send(f"{member.mention} What role do you want me to add? \n I haven't seen that reaction before. \n Let me remove it for you!", delete_after=10)
            await asyncio.sleep(3)
            await message.remove_reaction(payload.emoji.name, member)
            await self.channel.send(f"Done, Have a good day!", delete_after=6)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        print("role was triggered")
        guild = self.client.get_guild(payload.guild_id)
        if payload.emoji.name == "Giveaways" and payload.message_id == self.reaction_roles:
            role = discord.utils.get(guild.roles, name="Gw ping")
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                    await self.channel.send(f"{member.mention} I have removed The role Gw ping!", delete_after=10)
        elif payload.emoji.name == "Drops" and payload.message_id == self.reaction_roles:
            role = discord.utils.get(guild.roles, name="Drops ping")
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                    await self.channel.send(f"{member.mention} I have removed The role Drops Ping!", delete_after=10)

        elif payload.emoji.name == "blueannouncement" and payload.message_id == self.reaction_roles:
            print("got here")
            role = discord.utils.get(guild.roles, name="Announcement ping")
            if role is not None:
                print("found role")
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                print(f"member: {member}")
                if member is not None:
                    await member.remove_roles(role)
                    await self.channel.send(f"{member.mention} I have removed The role Announcement ping!", delete_after=10)

        elif payload.emoji.name == "L_chat" and payload.message_id == self.reaction_roles:
            print("got here")
            role = discord.utils.get(guild.roles, name="Dead chat ping")
            if role is not None:
                print("found role")
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                print(f"member: {member}")
                if member is not None:
                    await member.remove_roles(role)
                    await self.channel.send(f"{member.mention} I have removed The role Dead Chat ping!", delete_after=10)
        else:return

# Sends message with reaction
    @commands.command(hidden=True)
    async def react(self, ctx):
        message = discord.Embed(title=f'**Reation Roles**', description=f"<@&1081509778045550592> - <:Giveaways:1082165552665075804> \n <@&1082155989324791898> - <:Drops:1082165170018734130> \n <@&1081510006937100318> - <:blueannouncement:1082165628242235423> \n <@&1081509683447222332> - <:L_chat:1082166371326119957> \n \n <@&1081509778045550592> - Notifies you on all giveaways happening in the server.\n \n <@&1082155989324791898> - Notifies you on all the drops/quick drops happening in the server. \n \n <@&1081510006937100318> - Notifies you on our announcement and our updates. \n \n <@&1081509683447222332> - When chat goes dead, we need to revive it", color = discord.Color.from_rgb(16, 230, 194))
        react_messasge = await ctx.send(embed=message)
        await react_messasge.add_reaction("<:Giveaways:1082165552665075804>")
        await react_messasge.add_reaction("<:Drops:1082165170018734130>")
        await react_messasge.add_reaction("<:blueannouncement:1082165628242235423>")
        await react_messasge.add_reaction("<:L_chat:1082166371326119957>")


    
async def setup(client):
    await client.add_cog(Kingdom(client))