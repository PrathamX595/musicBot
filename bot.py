import discord
from discord.ext import commands
import dotenv
import os
dotenv.load_dotenv()

intent = discord.Intents.default()
intent.message_content = True
bot = commands.Bot(command_prefix='/', intents=intent)

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
            await voice_client.move_to(ctx.message.author.voice.channel)
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




bot.run(os.getenv('TOKEN'))