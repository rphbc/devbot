# bot.py
import asyncio
import os
import random
import re
import time
import traceback

import discord
import schedule
from decouple import Config, RepositoryEnv, AutoConfig
from discord.ext import commands

config = AutoConfig()
if os.environ.get("ENV"):
    config = Config(RepositoryEnv(os.environ.get("ENV", '.env')))


TOKEN = config('TOKEN')
AUTOR_ID = config('AUTOR_ID', cast=int)
VOICE_ID = config('VOICE_ID', cast=int)
WHITELISTED_SERVER_ID = config('WHITELISTED_SERVER_ID')
TEXT_CHN_ID = config('TEXT_CHN_ID', cast=int)
allowed_mentions = discord.AllowedMentions(everyone=True)
intents = discord.Intents.default()
intents.message_content=True
bot = commands.Bot(intents=intents, command_prefix='$')
loop = None

TOTO_MPEG = config('TOTO_MPEG_PATH')
FALOU_MP3 = config('FALOU_MP3_PATH')


@bot.command()
async def play(ctx, arg):
    if not bot.voice_clients:
        await ctx.send("No voice channel to play ;_;")
        return

    if arg == 'toto':
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(TOTO_MPEG)
        )
        ctx.voice_client.play(source)
        await ctx.send(
            f"IT'S TOTO TIME!!!:sunglasses: :beach_umbrella: :tada:"
        )

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


@play.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect(timeout=3)
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError(
                "Author not connected to a voice channel."
            )
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    print("Voice Connected")


@bot.command()
async def stop(ctx):
    bot.voice_clients[0].stop()
    await ctx.send(f"Stoping Music")


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    print(f"Joining Channel = {channel.id}")
    await channel.connect(reconnect=True)


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.event
async def on_ready():
    global loop
    print(f'{bot.user} connected. The power grows within BirminD!')
    print(f"Connected, list of channels: {list(bot.get_all_channels())}")

    # Set loop as global variable, so it can be used by scheduler
    # passing it as a variable wasn't working.
    loop = asyncio.get_event_loop()
    # loop.run_in_executor(None, schedule_job)
    loop.create_task(play_toto())


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
    print("Received Message is ", content)
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

    await bot.process_commands(
        message)  # So that events don't disable commands


async def alert_toto():
    channel_txt = bot.get_channel(TEXT_CHN_ID)
    await channel_txt.send(
        f"@everyone 15 minutos para o Toto Time!! :sunglasses:",
        allowed_mentions=allowed_mentions
    )


async def play_toto():
    print("Starting to play toto")
    channel = bot.get_channel(VOICE_ID)
    channel_txt = bot.get_channel(TEXT_CHN_ID)
    connection = await channel.connect()

    await channel_txt.send(
        f"@everyone IT'S TOTO TIME!!!:sunglasses: :beach_umbrella: :tada:",
        allowed_mentions=allowed_mentions
    )

    queue = [
        config("TOTO_MPEG_PATH"),
        config("FALOU_MP3_PATH")
    ]

    await asyncio.sleep(2)
    while connection.is_playing() or len(queue) > 0:
        if connection.is_playing():
            await asyncio.sleep(0.3)
            continue
        source = queue.pop(0)
        connection.play(
            discord.FFmpegPCMAudio(source),
            after=lambda e: print(f'Player error: {e}') if e else None
        )
        print("Playing "+ source)

    connection.stop()
    await connection.disconnect()

    # connection.play(
    #     # discord.FFmpegPCMAudio('metal_toto.mp3'),
    #     discord.FFmpegPCMAudio(config("TOTO_MPEG_PATH")),
    #     # discord.FFmpegPCMAudio('toto_june.mpeg'),
    #     after=lambda error: connection.play(
    #         discord.FFmpegPCMAudio(config("FALOU_MP3_PATH")),
    #         after=lambda error: connection.stop()
    #     ),
    # )



async def stop_toto():
    await bot.voice_clients[0].disconnect(force=True)


def run_task(task):
    asyncio.run_coroutine_threadsafe(task, loop)


def schedule_job():
    print("Starting Scheduler")
    schedule.every().friday.at(config("TOTO_ALERT_AT")).do(
        run_task, alert_toto()
    )
    schedule.every().friday.at(config("TOTO_PLAY_AT")).do(
        run_task, play_toto()
    )
    schedule.every().friday.at(config("TOTO_LEAVE_AT")).do(
        run_task, stop_toto()
    )

    while True:
        try:
            schedule.run_pending()
        except KeyboardInterrupt:
            return
        time.sleep(3)


if __name__ == "__main__":
    bot.run(TOKEN)
