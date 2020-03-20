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
    channel = member.channel
    await channel.send(
        f'{client.user} connected. The power grows within BirminD!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    if message.content == 'Oi Bot':
        response = f'Olá {message.author.nick}, seja bem-vindo(a)!'
        await message.channel.send(response)
    if message.content == 'Bom dia Bot':
        response = f'Bom dia mano.'
        await message.channel.send(response)
    if message.content == 'vai tomar no cu bot':
        response = f'Toma no cú é vitamina, como tu e tuas prima'
        await message.channel.send(response)


client.run(TOKEN)
