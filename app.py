import discord
import re
from discord.ext import commands
from discord.ui import Button
import random
import html2text
import aiohttp
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

@bot.tree.command(name='lcrandom', description='Fetch a random LeetCode problem!')
async def lcrandom(interaction: discord.Interaction):
    try:
        await interaction.response.defer()

        async with aiohttp.ClientSession() as session:
            url_total = 'https://alfa-leetcode-api.onrender.com/problems?limit=1'
            async with session.get(url_total) as response_total:
                data_total = await response_total.json()
            total_questions = data_total['totalQuestions']

            url = f'https://alfa-leetcode-api.onrender.com/problems?limit={total_questions}'
            async with session.get(url) as response:
                data = await response.json()

            random_problem = random.choice(data['problemsetQuestionList'])
            title_slug = random_problem['titleSlug']

            select_url = f'https://alfa-leetcode-api.onrender.com/select?titleSlug={title_slug}'
            async with session.get(select_url) as select_response:
                select_data = await select_response.json()

        problem_title = select_data['questionTitle']
        question_number = select_data['questionFrontendId']
        problem_difficulty = select_data['difficulty']
        problem_description = select_data['question']
        problem_description = re.sub(r'!\[\]\(.*?\)', '', problem_description)
        markdown_description = html_to_markdown(problem_description)
        problem_link = select_data['link']
        
        if problem_difficulty == 'Easy':
            color = 0x00B8A3  # Green
        elif problem_difficulty == 'Medium':
            color = 0xFFC01D  # Yellow
        elif problem_difficulty == 'Hard':
            color = 0xFF375F  # Red
        else:
            color = discord.Color.random()
        embed = discord.Embed(title=f"{question_number}. {problem_title}", description=f"**Difficulty:** {problem_difficulty}\n**Description:** {markdown_description}", color=color)
        button = Button(style=discord.ButtonStyle.link, label="Solve", url=problem_link)  # Create a Button
        view = discord.ui.View()
        view.add_item(button)

        await interaction.followup.send(embed=embed, view=view)
    except Exception as e:
        await interaction.followup.send(f'Failed to fetch a random LeetCode problem. Error: {e}')

def html_to_markdown(html_text):
    markdown_text = html2text.html2text(html_text)
    markdown_text = markdown_text.replace("![](", "").replace(")", "")
    return markdown_text

bot.run(token)