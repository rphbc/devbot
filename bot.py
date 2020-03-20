# bot.py

import random
import re

import discord
from decouple import config

TOKEN = config('TOKEN')

client = discord.Client()


# channel id is 690226588696051796

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
    author = message.author
    channel = message.channel
    content = message.content.lower()
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await channel.send(response)
    if content == 'Oi Bot'.lower():
        response = f'Olá {author.display_name}, seja bem-vindo(a)!'
        await channel.send(response)
    if re.search(r'^(bom\s?dia.*?bot)', content):
        response = f'Bom dia mano.'
        await channel.send(response)
    if content == 'vai tomar no cu bot'.lower():
        response = f'Toma no cú é vitamina, como tu e tuas prima'
        await channel.send(response)


client.run(TOKEN)
