# bot.py
import os

import discord
import random
from decouple import config

# load_dotenv()
from devbot.commands.greetings import GreetCommand
from devbot.core.routers import Route
from devbot.core.runner import execute_command

TOKEN = config('TOKEN')

client = discord.Client()

routes = [
    Route('example', GreetCommand)
]

@client.event
async def on_ready():
    print(f'{client.user} connected. The power grows within BirminD!')


@client.event
async def on_member_join(member):
    channel = member.channel
    await channel.send(
        f'{client.user} connected. The power grows within BirminD!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    response = execute_command(routes, message.content)
    if response:
        await message.channel.send(response)


client.run(TOKEN)
