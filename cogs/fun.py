import os
import discord
import time
import datetime
import asyncio
import random
import json
from discord import app_commands
from discord.ext import commands
class fun(commands.GroupCog):

    def __init__(self,client):
        self.client = client

    @app_commands.command(description= "Beg people to give you coins")
    @app_commands.checks.cooldown(1,45)
    async def beg(self, interaction: discord.Interaction):
        await self.open_account(interaction.user)
        users = await self.get_bank_data()
        user = interaction.user
        earnings = random.randrange(451)
        em1 = (f"The developer gave you {earnings} coins!! You must be lucky")
        em2 = (f"A person that walked up to your front door gave you a package with {earnings} coins in it. Wow what a treat!!")
        em3 = (f'You have bad luck you got nothing.')
        begthem = [em1, em2, em3]
        await interaction.response.send_messsage(random.choice(begthem))
        users = await self.get_bank_data()
        users[str(user.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users, f)

    @app_commands.command(description="Alows you to work for coins")
    @app_commands.checks.cooldown(1,21600)
    async def work(self, interaction: discord.Interaction):
        await self.open_account(interaction.user)
        users = await self.get_bank_data()
        user = interaction.user
        earnings = random.randint(100,5000)
        em = discord.Embed(title = "McDonald's Worker", description=f"You worked as a McDonald's worker and you got {earnings} for your day of work!!")
        await interaction.response.send_message(embed = em)
        users[str(user.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users, f)
    @app_commands.command(name='daily')
    @app_commands.checks.cooldown(1,86400)
    async def daily(self, interaction: discord.Interaction):
        await self.open_account(interaction.user)
        users = await self.get_bank_data()
        user = interaction.user
        earnings = 15000
        em = discord.Embed(title = f"{interaction.user.name}'s daily ammount", description=f"You got **{earnings}** coins from your daily salery for being in the server!")
        await interaction.response.send_message(embed = em)
        users[str(user.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users, f)
        

    @commands.Cog.listener()
    async def on_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = "**Still on cooldown!!!**, please try again in {:.2f}s".format(error.retry_after)
            await interaction.response.send_message(msg, delete_after = 10)
            await asyncio.sleep(10)
            await interaction.message.delete()

    @app_commands.command(description= "Gives you a random number between 50 and 150")
    async def number(self, interaction: discord.Interaction):
        Number = random.randint(50, 150)
        await interaction.response.send_message(Number)
    @app_commands.command()
    async def bal(self, interaction: discord.Interaction):
        await self.open_account(interaction.user)
        user = interaction.user
        users = await self.get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]
        
        em = discord.Embed(title = f"{interaction.user.name}'s balance", color = discord.Color.green())
        em.add_field(name = "Wallet", value =wallet_amt)
        em.add_field(name = "Bank", value =bank_amt)
        await interaction.response.send_message(embed = em)

    @app_commands.command()
    @app_commands.describe(amount="The amount to withdraw")
    async def withdraw(self, interaction: discord.Interaction, amount: int):
        await self.open_account(interaction.user)
        if amount == None:
            await interaction.response.send_message("please enter the amount to withdraw!")
        bal = await self.update_bank(interaction.user)
        amount = int(amount)
        if amount>bal[1]:
            await interaction.response.send_message("Your not that rich!")
            return
        if amount<0:
            await interaction.response.send_message("Amount must be greater than zero!")
            return
        await self.update_bank(interaction.user,amount)
        await self.update_bank(interaction.user,-1*amount, "bank")
        await interaction.response.send_message(f"You withdrew {amount} coins")


    @app_commands.command()
    @app_commands.describe(amount="The amount you want to desposit")
    async def desposit(self, interaction: discord.Interaction, amount: int):
        await self.open_account(interaction.user)
        if amount == None:
            await interaction.response.send_message("please enter the amount to desposit!")
        bal = await self.update_bank(interaction.user)
        amount = int(amount)
        if amount>bal[0]:
            await interaction.response.send_message("Your not that rich!")
            return
        if amount<0:
            await interaction.response.send_message("Amount must be greater than zero!")
            return
        await self.update_bank(interaction.user,-1*amount)
        await self.update_bank(interaction.user,amount, "bank")
        await interaction.response.send_message(f"You deposited {amount} coins")

    @app_commands.command()
    @app_commands.describe(amount="The amount you want to withdraw")
    async def empty(self, interaction: discord.Interaction, amount: int):
        await self.open_account(interaction.user)
        if amount == None:
            await interaction.response.send_message("please enter the amount to withdraw!")
        bal = await self.update_bank(interaction.user)
        amount = int(amount)
        if amount>bal[1]:
            await interaction.response.send_message("Your not that rich!")
            return
        if amount<0:
            await interaction.response.send_message("Amount must be greater than zero!")
            return
        await self.update_bank(interaction.user,amount)
        await self.update_bank(interaction.user,-1*amount, "bank")
        await interaction.response.send_message(f"You emptied {amount} coins from your bank account! I wonder why you did it.")

    @app_commands.command(description= "Give money to a user")
    @app_commands.describe(member= "The member you want to give money to")
    @app_commands.describe(amount= "The amount you want to give")
    async def give(self, interaction: discord.Interaction,member:discord.Member, amount: int):
        await self.open_account(interaction.user)
        await self.open_account(member)
        if amount == None:
            await interaction.response.send_message("please enter the amount to give!")
        bal = await self.update_bank(interaction.user)
        amount = int(amount)
        if amount>bal[0]:
            await interaction.response.send_message("Your not that rich!")
            return
        if amount<0:
            await interaction.response.send_message("Amount must be greater than zero!")
            return
        await self.update_bank(interaction.user, -1*amount)
        await self.update_bank(member,amount)
        await interaction.response.send_message(f"You gave {amount} coins to {member}!!")

    @app_commands.command(description="gamble your money!")
    @app_commands.describe(amount="The amount you want to Gamble")
    async def slots(self, interaction: discord.Interaction, amount: int):
        await self.open_account(interaction.user)
        if amount == None:
            await interaction.response.send_message("please enter the amount!")
        bal = await self.update_bank(interaction.user)
        amount = int(amount)
        if amount>bal[0]:
            await interaction.reponse.send_message("Your not that rich!")
            return
        if amount<0:
            await interaction.response.send_message("Amount must be greater than zero!")
            return
        final = []
        for i in range(3):
            a = random.choice(["x","o","Q"])

            final.append(a)



        if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
            await self.update_bank(interaction.user,1*amount)
            await interaction.response.send_message(f"{str(final)} \n You won!")
        else: 
            await self.update_bank(interaction.user,-1*amount)
            await interaction.response.send_message(f"{str(final)} \nYou lost.")

        
    @app_commands.command(description="Shows the items in the shop")
    async def shop(self, interaction: discord.Interaction):
    
        em = discord.Embed(title = "Shop")

        for item in self.mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name = name, value = f"${price} | {desc}")

        await interaction.response.send_message(embed= em)

    @app_commands.command()
    @app_commands.describe(item="The item you want to buy")
    @app_commands.describe(amount="The amount you want to buy")
    async def buy(self, interaction: discord.Interaction,item: str,amount: int = 1):
        await self.open_account(interaction.user)
        user = interaction.user
        res = await self.buy_this(interaction, user, item, amount)

        if not res[0]:
            if res[1]==1:
                await interaction.response.send_message("That item isn't there!")
                return
            if res[1] ==2:
                await interaction.response.send_message(f"You don't have enough coins in your wallet to buy {amount}") 
                return
        await interaction.response.send_message(f"You just bought {amount} {item}")

    @app_commands.command(description="Shows the contents of your bag")
    async def bag(self, interaction: discord.Interaction):
        await self.open_account(interaction.user)
        user = interaction.user
        users = await self.get_bank_data()
        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em = discord.Embed(title = "bag")
        for item in bag:
            name = item["item"]
            amount = item["amount"]
            em.add_field(name = name, value = amount)
        await interaction.response.send_message(embed = em)
    @app_commands.command(description="Sells an item back to the shop")
    @app_commands.describe(item="The item you want to sell")
    @app_commands.describe(amount="The amount of the items you want to sell")
    async def sell(self,interaction: discord.Interaction,item: str,amount: int = 1):
        await self.open_account(ctx.author)

        res = await self.sell_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("That Object isn't there!")
                return
            if res[1]==2:
                await ctx.send(f"You don't have {amount} {item} in your bag.")
                return
            if res[1]==3:
                await ctx.send(f"You don't have {item} in your bag.")
                return

            await ctx.send(f"You just sold {amount} {item}.")

    @app_commands.command(description="Shows who is the richest")
    async def leaderboard(self,interaction: discord.Interaction,):
        x = 10
        users = await self.get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total,reverse=True)    

        em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = self.client.get_user(id_)
            name = member.name
            em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
            if index == x:
                break
        else:
            index += 1

        await interaction.response.send_message(embed = em)
               


#__________________________________________________________________


    async def open_account(self, user):

        users = await self.get_bank_data()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["wallet"] = 0
            users[str(user.id)]["bank"] = 0

        with open("mainbank.json","w") as f:
            users = json.dump(users, f)
        return True

    async def get_bank_data(self):
        with open("mainbank.json","r") as f:
     
            users = json.load(f)
        return users

    async def update_bank(self, user,change = 0,mode ="wallet"):
        users = await self.get_bank_data()

        users[str(user.id)][mode] +=change

        with open("mainbank.json","w") as f:
            json.dump(users, f)


        bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
        return bal
    
    mainshop = [{"name":"cheese","price":1000,"description": "cheese: decreases command cool down by 1 second!"},
    {"name":"carrot","price":1500,"description": "carrot:increases the amount of coins you get by 50."},
    {"name":"apple","price":2000,"description": "apple: gives you more luck"},
    {"name":"bread","price":2500,"description": "bread: Makes someone lose money"},
    {"name":"beer","price":3000,"description": "Makes your cooldown time less but you suffer more if you drink to much"},
    {"name":"Silicon","price":50000,"description": "daily reward increases by 15,000 (Daily reward not yet implemented so just save them)"}]

    async def buy_this(self,interaction: discord.Interaction,user,item_name,amount):
        item_name = item_name.lower()
        name_ = None
        for item in self.mainshop:
            name = item["name"].lower()
            name_ = name
            price = item["price"]
            break
        if name == None:
            return [False,1]
        cost = price*amount
        users = await self.get_bank_data()
        bal = await self.update_bank(user)
        if bal[0]<cost:
            return [False,2]

        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt + amount
                    users[str(user.id)]["bag"][index]["amount"] = new_amt
                    t = 1
                    break
                index==1
            if t == None:
                obj = {"item": item_name , "amount" : amount}
                users[str(user.id)]["bag"] = [obj]
        except:
            obj = {"item": item_name , "amount" : amount}
            users[str(user.id)]["bag"] = [obj]

        with open("mainbank.json","w") as f:
            json.dump(users,f)

        await self.update_bank(user,cost*-1,"wallet")

        return [True, "worked"]


    async def sell_this(self,user,item_name,amount,price = None):
        item_name = item_name.lower()
        name_ = None
        for item in self.mainshop:
            name = item["name"].lower()
            if name == item_name:
                name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

        if name_ == None:
            return [False,1]

        cost = price*amount

        users = await self.get_bank_data()

        bal = await self.update_bank(user)


        try:
            index = 0
            t = None
            for thing in users[str(user.id)]["bag"]:
                n = thing["item"]
                if n == item_name:
                    old_amt = thing["amount"]
                    new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
            if t == None:
                return [False,3]
        except:
            return [False,3]    

        with open("mainbank.json","w") as f:
            json.dump(users,f)

        await self.update_bank(user,cost,"wallet")

        return [True,"Worked"]



async def setup(client):
     await client.add_cog(fun(client)) 
