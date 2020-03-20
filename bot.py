# bot.py
import os

import discord
import random
from decouple import config

# load_dotenv()
TOKEN = config('TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} connected. The power grows within BirminD!')


@client.event
async def on_member_join(member):
    await member.send(
        f'{member.display_name} connected. The power grows within BirminD!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    channel = message.channel
    message = message.content.lower()
    print(message)
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message == '99!':
        response = random.choice(brooklyn_99_quotes)
        await channel.send(response)
    if message == 'Oi Bot'.lower():
        response = f'Olá {message.author.display_name}, seja bem-vindo(a)!'
        await channel.send(response)
    if message == 'Bom dia Bot'.lower():
        response = f'Bom dia mano.'
        await channel.send(response)
    if message == 'vai tomar no cu bot'.lower():
        response = f'Toma no cú é vitamina, como tu e tuas prima'
        await channel.send(response)


client.run(TOKEN)
