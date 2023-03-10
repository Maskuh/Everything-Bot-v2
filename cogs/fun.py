import os
import discord
import time
import datetime
import asyncio
import random
import json
from discord.ext import commands

class fun(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command(name='beg')
    @commands.cooldown(1,45,commands.BucketType.user)
    async def beg(self, ctx):
        await self.open_account(ctx.author)
        users = await self.get_bank_data()
        user = ctx.author
        earnings = random.randrange(451)
        em1 = (f"The developer gave you {earnings} coins!! You must be lucky")
        em2 = (f"A person that walked up to your front door gave you a package with {earnings} coins in it. Wow what a treat!!")
        em3 = (f'You have bad luck you got nothing.')
        begthem = [em1, em2, em3]
        await ctx.channel.send(random.choice(begthem))
        users = await self.get_bank_data()
        users[str(user.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users, f)

    @commands.command(name='Work')
    @commands.cooldown(1,21600,commands.BucketType.user)
    async def Work(self,ctx):
        await self.open_account(ctx.author)
        users = await self.get_bank_data()
        user = ctx.author
        earnings = random.randint(100,5000)
        em = discord.Embed(title = "McDonald's Worker", description=f"You worked as a McDonald's worker and you got {earnings} for your day of work!!")
        await ctx.channel.send(embed = em)
        users[str(user.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users, f)
    @commands.command(name='daily')
    @commands.cooldown(1,86400, commands.BucketType.user)
    async def daily(self, ctx):
        await self.open_account(ctx.author)
        users = await self.get_bank_data()
        user = ctx.author
        earnings = 15000
        em = discord.Embed(title = f"{ctx.author.name}'s daily ammount", description=f"You got **{earnings}** coins from your daily salery for being in the server!")
        await ctx.channel.send(embed = em)
        users[str(user.id)]["wallet"] += earnings
        with open("mainbank.json","w") as f:
            json.dump(users, f)
        

    #@commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = "**Still on cooldown!!!**, please try again in {:.2f}s".format(error.retry_after)
            await ctx.send(msg, delete_after = 10)
            await asyncio.sleep(10)
            await ctx.message.delete()

    @commands.command(name='Number')
    async def Number(self, ctx):
        Number = random.randint(50, 150)
        await ctx.channel.send(Number)
    @commands.command()
    async def bal(self, ctx):
        await self.open_account(ctx.author)
        user = ctx.author
        users = await self.get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]
        
        em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.green())
        em.add_field(name = "Wallet", value =wallet_amt)
        em.add_field(name = "Bank", value =bank_amt)
        await ctx.send(embed = em)

    @commands.command()
    async def withdraw(self, ctx, amount = None, aliases = ["with"]):
        await self.open_account(ctx.author)
        if amount == None:
            await ctx.send("please enter the amount to withdraw!")
        bal = await self.update_bank(ctx.author)
        amount = int(amount)
        if amount>bal[1]:
            await ctx.send("Your not that rich!")
            return
        if amount<0:
            await ctx.send("Amount must be greater than zero!")
            return
        await self.update_bank(ctx.author,amount)
        await self.update_bank(ctx.author,-1*amount, "bank")
        await ctx.send(f"You withdrew {amount} coins")


    @commands.command(aliases = ["dep"])
    async def desposit(self, ctx, amount = None):
        await self.open_account(ctx.author)
        if amount == None:
            await ctx.send("please enter the amount to desposit!")
        bal = await self.update_bank(ctx.author)
        amount = int(amount)
        if amount>bal[0]:
            await ctx.send("Your not that rich!")
            return
        if amount<0:
            await ctx.send("Amount must be greater than zero!")
            return
        await self.update_bank(ctx.author,-1*amount)
        await self.update_bank(ctx.author,amount, "bank")
        await ctx.send(f"You deposited {amount} coins")

    @commands.command()
    async def empty(self, ctx, amount = None):
        await self.open_account(ctx.author)
        if amount == None:
            await ctx.send("please enter the amount to withdraw!")
        bal = await self.update_bank(ctx.author)
        amount = int(amount)
        if amount>bal[1]:
            await ctx.send("Your not that rich!")
            return
        if amount<0:
            await ctx.send("Amount must be greater than zero!")
            return
        await self.update_bank(ctx.author,amount)
        await self.update_bank(ctx.author,-1*amount, "bank")
        await ctx.send(f"You emptied {amount} coins from your bank account! I wonder why you did it.")

    @commands.command()
    async def give(self, ctx,member:discord.Member, amount = None):
        await self.open_account(ctx.author)
        await self.open_account(member)
        if amount == None:
            await ctx.send("please enter the amount to give!")
        bal = await self.update_bank(ctx.author)
        amount = int(amount)
        if amount>bal[0]:
            await ctx.send("Your not that rich!")
            return
        if amount<0:
            await ctx.send("Amount must be greater than zero!")
            return
        await self.update_bank(ctx.author, -1*amount)
        await self.update_bank(member,amount)
        await ctx.send(f"You gave {amount} coins to {member}!!")

    @commands.command()
    async def slots(self, ctx, amount):
        await self.open_account(ctx.author)
        if amount == None:
            await ctx.send("please enter the amount!")
        bal = await self.update_bank(ctx.author)
        amount = int(amount)
        if amount>bal[0]:
            await ctx.send("Your not that rich!")
            return
        if amount<0:
            await ctx.send("Amount must be greater than zero!")
            return
        final = []
        for i in range(3):
            a = random.choice(["x","o","Q"])

            final.append(a)


        await ctx.send(str(final))

        if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
            await self.update_bank(ctx.author,1*amount)
            await ctx.send("You won!")
        else: 
            await self.update_bank(ctx.author,-1*amount)
            await ctx.send("You lost.")

        
    @commands.command()
    async def shop(self, ctx):
    
        em = discord.Embed(title = "Shop")

        for item in self.mainshop:
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name = name, value = f"${price} | {desc}")

        await ctx.send(embed= em)

    @commands.command()
    async def buy(self, ctx,item,amount = 1):
        await self.open_account(ctx.author)
        user = ctx.author
        res = await self.buy_this(ctx, user, item, amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("That item isn't there!")
                return
            if res[1] ==2:
                await ctx.send(f"You don't have enough coins in your wallet to buy {amount}") 
                return
        await ctx.send(f"You just bought {amount} {item}")

    @commands.command()
    async def bag(self, ctx):
        await self.open_account(ctx.author)
        user = ctx.author
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
        await ctx.send(embed = em)
    @commands.command()
    async def sell(self,ctx,item,amount = 1):
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

    @commands.command(aliases = ["lb"])
    async def leaderboard(self,ctx,x = 10):
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

        await ctx.send(embed = em)
               


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

    async def buy_this(self,ctx,user,item_name,amount):
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
