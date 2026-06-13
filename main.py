import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import asyncio
import datetime
import random
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

private_role = "Tester Role"

@bot.event
async def on_ready():
     print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
     await member.channel.send(f'Welcome to the town!! {member.name}!')

@bot.event
async def on_message(message):
     if message.author == bot.user:
          return

     if "faggot" in message.content.lower():
         await message.delete()
         await message.channel.send(f'{message.author.mention} Please watch your language here')

     await bot.process_commands(message)

@bot.command()
async def hello(ctx):
     await ctx.send(f'Hello {ctx.author.mention}!')

@bot.command()
async def assign(ctx):
     role = discord.utils.get(ctx.guild.roles, name=private_role)
     if role:
         await ctx.author.add_roles(role)
         await ctx.author.send(f"{ctx.author.mention} was given the private role {private_role}")

     else:
          await ctx.send("Role Does Not Exist")

@bot.command()
async def remove(ctx):
     role = discord.utils.get(ctx.guild.roles, name=private_role)
     if role:
         await ctx.author.remove_roles(role)
         await ctx.author.send(f"{ctx.author.mention} no longer has the role {private_role}")

     else:
          await ctx.send("BeeBot has flown into an issue here")

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(f"{message}")

@bot.command()
@commands.has_role(private_role)
async def private(ctx):
    await ctx.send("You know the secret Martha!!!")

@private.error
async def private_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("YOU WILL NEVER KNOW!!!")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New!! Poll", description=question, color=discord.Color.green())
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
async def surprise(ctx):
    embed = discord.Embed(title="HAPPY BIRTHDAY", description=f"I hope you had a sweet as honey birthday!{ctx.author.mention}", color=discord.Color.yellow())
    birthday_message = await ctx.send(embed=embed)
    await birthday_message.add_reaction("🎂")
    await birthday_message.add_reaction("🎉")

@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="commands", description = "$surprise[send a birthday message], $poll[create a yes/no poll], $say[make BeeBot say what you want them too], $hello[BeeBot says hello too] ", color=discord.Color.green())
    commands_message = await ctx.send(embed=embed)
    await  commands_message.send()

bot.run(token, log_handler=handler, log_level=logging.DEBUG)