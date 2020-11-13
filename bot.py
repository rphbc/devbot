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

loop = asyncio.get_event_loop()
bot = commands.Bot(command_prefix='$')


@bot.command()
async def play(ctx, arg):
    print(dir(ctx.author))
    if not bot.voice_clients:
        await ctx.send("No voice channel to play ;_;")
        return

    if ctx.author.id != 619319443905839126:
        await ctx.send("You can't fool me, you don't have the rights to do "
                       "that")
        return

    if arg == 'toto':
        bot.voice_clients[0].play(discord.FFmpegPCMAudio('10. Africa.mp3'))
        print(bot.voice_clients[0])
        await ctx.send(f"IT'S TOTO TIME!!!:sunglasses: :beach_umbrella: :tada:")
        await ctx.send(f"Playing {arg}")
    else:
        await ctx.send(f"No music called {arg}")


@bot.command()
async def stop(ctx):
    bot.voice_clients[0].stop()
    await ctx.send(f"Stoping Music")


# voice channel 700865335057711234
@bot.command()
async def join(ctx):
    # channel = ctx.author.voice.channel
    id_chn = 700865335057711234
    channel = bot.get_channel(id_chn)
    # await discord.Client.join_voice_channel(channel)

    await channel.connect()


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

# channel id is 690226588696051796

# @bot.command(
#     name='vuvuzela',
#     description='Plays an awful vuvuzela in the voice channel',
#     pass_context=True,
# )
# async def vuvuzela(context):
#     # grab the user who sent the command
#     user = context.message.author
#     voice_channel = user.voice.voice_channel
#     channel = None
#     # only play music if user is in a voice channel
#     if voice_channel is not None:
#         # grab user's voice channel
#         channel = voice_channel.name
#         await context.send('User is in channel: '+ channel)
#         # create StreamPlayer
#         vc = await bot.join_voice_channel(voice_channel)
#         player = vc.create_ffmpeg_player('vuvuzela.mp3', after=lambda: print('done'))
#         player.start()
#         while not player.is_done():
#             await asyncio.sleep(1)
#         # disconnect after the player has finished
#         player.stop()
#         await vc.disconnect()
#     else:
#         await bot.say('User is not in a channel.')

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

    WHITELISTED_SERVER_ID = 708336769409744939
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

    await bot.process_commands(message)  #So that events don't disable commands


def play_toto():

    id_chn = 700865335057711234
    channel_voice = bot.get_channel(id_chn)
    loop.run_until_complete(channel_voice.connect())
    # await channel_voice.connect()
    time.sleep(2)
    id_chn_txt = 690226588696051796
    channel_txt = bot.get_channel(id_chn_txt)

    bot.voice_clients[0].play(discord.FFmpegPCMAudio('10. Africa.mp3'))
    loop.run_until_complete(channel_txt.send(f"IT'S TOTO TIME!!!:sunglasses: "
                                             f":beach_umbrella: :tada:"))
    print(" schedule funciona")


# async def play_memo():
#     id_chn = 700865335057711234
#     channel_voice = bot.get_channel(id_chn)
#     await channel_voice.connect()


def stop_toto():
    bot.voice_clients[0].stop()
    loop.run_until_complete(bot.voice_clients[0].disconnect())


def schedule_job():
    schedule.every().friday.at("18:00").do(play_toto)
    schedule.every().friday.at("18:10").do(stop_toto)
    while True:
        schedule.run_pending()
        time.sleep(3)


if __name__ == "__main__":
    bot_thread = Thread(target=schedule_job)
    bot_thread.start()
    bot.run(TOKEN)


# 690226588696051796