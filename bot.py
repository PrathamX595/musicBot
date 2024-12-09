import discord
from discord.ext import commands
import dotenv
import os
import yt_dlp as youtube_dl
from yt_dlp import YoutubeDL
import asyncio
from discord.utils import get
from discord import FFmpegPCMAudio
dotenv.load_dotenv()

intent = discord.Intents.default()
intent.message_content = True
bot = commands.Bot(command_prefix='/', intents=intent)
list = []

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='join')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        voice_client = ctx.message.guild.voice_client
        if voice_client:
            await ctx.send("I am already in a voice channel")
            return
        else:
            channel = ctx.message.author.voice.channel
            await channel.connect()

@bot.command(name='leave')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    members = len(voice_client.channel.members)
    if members > 1:
        if(ctx.message.author.voice.channel == voice_client.channel):
            await voice_client.disconnect()
            return
        else:
            await ctx.send("you really think I am that stupid?")
    elif voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='pause')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    
@bot.command(name='next')
async def next(ctx, url):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        if ctx.author.voice:
            list.append(url)
            print(list)
        else:
            await ctx.send("You are not connected to a voice channel.")
            return
    else:
        await ctx.send("the bot isn't playing rn")

@bot.command(name='resume')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()

@bot.command()
async def play(ctx, url):
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    list.append(url)

    if not voice:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            return

    if not voice.is_playing():
        await playNext(ctx)

async def playNext(ctx):
    if len(list) > 0:
        url = list.pop(0)
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
        voice = get(bot.voice_clients, guild=ctx.guild)

        try:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(playNext(ctx), bot.loop))
            await ctx.send(f'Bot is playing: {info["title"]}')
        except Exception as e:
            await ctx.send("An error occurred")
            await playNext(ctx)
    else:
        await ctx.send("Queue is empty")

bot.run(os.getenv('TOKEN'))