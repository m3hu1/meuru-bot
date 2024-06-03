import discord
from discord.ext import commands
from discord import app_commands
import json
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('DISCORD_BOT_TOKEN')
if not token:
    raise ValueError("No token found! Please set the DISCORD_BOT_TOKEN environment variable.")

bot = commands.Bot(command_prefix=';', intents=discord.Intents.all())

@bot.event
async def on_ready():
    try:
        s = await bot.tree.sync()
        print(f'Synced {len(s)} commands')
    except Exception as e:
        print(f'Error syncing commands: {e}')
    
    print(f'Logged in as {bot.user.name}')
    
# @bot.tree.command(name='hello', description='Hello World!')
# async def hello(interaction: discord.Interaction):
#     await interaction.response.send_message('Hello World!')
    
# @bot.tree.command(name='ping', description='Display the latency of the bot!')
# async def ping(interaction: discord.Interaction):
#     await interaction.response.send_message(f'Pong! ||{round(bot.latency * 1000)}ms||')
    
# @bot.tree.command(name='say', description='I\'ll repeat what you want to say!')
# @app_commands.describe(what_to_say='The message you want me to say!')
# async def say(interaction: discord.Interaction, what_to_say: str):
#     await interaction.response.send_message(f'{what_to_say} - **{interaction.user.display_name}**')

@bot.tree.command(name='brawlping', description='Ping Brawlhalla server and show the result')
async def brawlping(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
        
        result = subprocess.run(['ping', 'pingtest-sgp.brawlhalla.com', '-c', '4'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            await interaction.followup.send(f'```{result.stdout}```')
        else:
            await interaction.followup.send(f'Error: ```{result.stderr}```')
    except Exception as e:
        await interaction.followup.send(f'An error occurred: {e}')

bot.run(token)
