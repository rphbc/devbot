# bot.py
import logging

import discord
from decouple import config

# load_dotenv()
from devbot.commands.greetings import GreetCommand
from devbot.core.routers import Route, get_devbot_route
from devbot.core.runner import execute_command

TOKEN = config('TOKEN')
logger = logging.getLogger(__name__)

routes = get_devbot_route(
    Route('greeter', GreetCommand),
)


client = discord.Client()


@client.event
async def on_ready():
    logger.info(f'{client.user} connected.')


@client.event
async def on_member_join(member):
    logger.info(f'{member.name} connected to {member.channel}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    response = await execute_command(routes, message)
    if response:
        await message.channel.send(response)


client.run(TOKEN)
