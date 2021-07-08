# bot.py
import asyncio
import random
import re
import time
import traceback
from threading import Thread

import discord
import schedule
from discord.ext import commands

from decouple import config

import nest_asyncio

nest_asyncio.apply()

TOKEN = config('TOKEN')
CHANNEL_ID = config('CHANNEL_ID')
AUTOR_ID = config('AUTOR_ID')
VOICE_ID = config('VOICE_ID')
WHITELISTED_SERVER_ID = config('WHITELISTED_SERVER_ID')
TEXT_CHN_ID = config('TEXT_CHN_ID')

loop = asyncio.get_event_loop()
bot = commands.Bot(command_prefix='$')


@bot.command()
async def play(ctx, arg):
    print(dir(ctx.author))
    if not bot.voice_clients:
        await ctx.send("No voice channel to play ;_;")
        return

    if ctx.author.id != AUTOR_ID:
        await ctx.send("You can't fool me, you don't have the rights to do "
                       "that")
        return

    if arg == 'toto':
        bot.voice_clients[0].play(discord.FFmpegPCMAudio('10. Africa.mp3'))
        # bot.voice_clients[0].play(
        #     discord.FFmpegPCMAudio('Rick Astley - Never Gonna Give You Up.mp3'))
        print(bot.voice_clients[0])
        await ctx.send(f"IT'S TOTO TIME!!!:sunglasses: :beach_umbrella: :tada:")
        await ctx.send(f"Playing {arg}")
    elif arg == 'roda':
        bot.voice_clients[0].play(discord.FFmpegPCMAudio(
            'Pra_Ganhar_e_So_Rodar_Bau_da_Felicidade_-_Musica_tema_Original_Completa_50k.mp3'))
        # bot.voice_clients[0].play(
        #     discord.FFmpegPCMAudio('Rick Astley - Never Gonna Give You Up.mp3'))
        print(bot.voice_clients[0])
        await ctx.send(f"Roda a Rooooooda...")
        # await ctx.send(f"Playing {arg}")
    else:
        await ctx.send(f"No music called {arg}")


@bot.command()
async def stop(ctx):
    bot.voice_clients[0].stop()
    await ctx.send(f"Stoping Music")


@bot.command()
async def join(ctx):
    # channel = ctx.author.voice.channel
    id_chn = VOICE_ID
    channel = bot.get_channel(id_chn)
    # await discord.Client.join_voice_channel(channel)

    await channel.connect()


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.event
async def on_ready():
    print(f'{bot.user} connected. The power grows within BirminD!')


@bot.event
async def on_member_join(member):
    await member.send(
        f'{member.display_name} connected. The power grows within BirminD!')


@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if message.channel.guild.id == WHITELISTED_SERVER_ID:
        try:
            print(dir(bot.voice_clients[0]))
        except:
            traceback.print_exc()

    author = message.author
    channel = message.channel
    print(channel.id)
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

    await bot.process_commands(message)  # So that events don't disable commands


def play_toto():
    id_chn = VOICE_ID
    channel_voice = bot.get_channel(id_chn)
    loop.run_until_complete(channel_voice.connect())
    # await channel_voice.connect()
    time.sleep(2)
    id_chn_txt = TEXT_CHN_ID
    channel_txt = bot.get_channel(id_chn_txt)

    bot.voice_clients[0].play(discord.FFmpegPCMAudio('10. Africa.mp3'))
    # bot.voice_clients[0].play(discord.FFmpegPCMAudio('Rick Astley - Never Gonna Give You Up.mp3'))
    loop.run_until_complete(channel_txt.send(f"IT'S TOTO TIME!!!:sunglasses: "
                                             f":beach_umbrella: :tada:"))


def stop_toto():
    bot.voice_clients[0].stop()
    loop.run_until_complete(bot.voice_clients[0].disconnect())


def schedule_job():
    # schedule.every().friday.at("18:00").do(play_toto)
    # schedule.every().friday.at("18:10").do(stop_toto)

    schedule.every().friday.at("18:00").do(play_toto)
    schedule.every().friday.at("18:10").do(stop_toto)
    while True:
        schedule.run_pending()
        time.sleep(3)


if __name__ == "__main__":
    bot_thread = Thread(target=schedule_job)
    bot_thread.start()
    bot.run(TOKEN)

