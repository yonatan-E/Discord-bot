import discord
from discord.ext import commands
from discord.utils import get

import youtube_dl
import requests

from util.error_handling import send_command_error_message

class music_operations(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot

        self.__song_queue = []
        self.__song_details = {}

    @commands.command(aliases=['connect'], help='Make the bot to join to the current voice channel.')
    async def join(self, ctx):
        member_voice_status = ctx.author.voice

        if not member_voice_status:
            await send_command_error_message(ctx, 'Please connect to a voice channel before doing this command.')

        else:
            bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

            if bot_voice_client and bot_voice_client.channel.id != member_voice_status.channel.id:
                await send_command_error_message(ctx, f'{self.__bot.user.name} is already connected to another voice channel.')
            else:
                try:
                    await member_voice_status.channel.connect()
                except:
                    pass

    @commands.command(aliases=['disconnect'], help='Make the bot to leave the current voice channel.')
    async def leave(self, ctx):
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if bot_voice_client:
            await bot_voice_client.disconnect()
        else:
            await send_command_error_message(ctx, f'Please join {self.__bot.user.name} to a voice channel before making it leave one.')

    def search(self, arg):
        try: requests.get("".join(arg))
        except: arg = " ".join(arg)
        else: arg = "".join(arg)
        with youtube_dl.YoutubeDL(YDL_OPTIONS ) as ydl:
            info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, song_name):
        YDL_OPTS = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        song_url = song_name
        if song_url not in self.__song_queue:
            with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
                info = ydl.extract_info(song_url, download=False)

                self.__song_queue.append(song_url)
                self.__song_details[song_url] = {'url': info['url'], 'title': info['title']}
        
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await self.join(ctx)
            bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)
        
        if bot_voice_client.is_connected() and not bot_voice_client.is_playing():
            bot_voice_client.play(discord.FFmpegPCMAudio(self.__song_details[song_url]['url']), after=lambda e: self.play_next(ctx))

    def play_next(self, ctx):
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)
        if len(self.__song_queue) > 1:
            popped = self.__song_queue.pop()
            bot_voice_client.play(discord.FFmpegPCMAudio(self.__song_details[popped]['url']), after=lambda e: self.play_next(ctx))

    @commands.command()
    async def pause(self, ctx):
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if bot_voice_client and bot_voice_client.is_playing():
            bot_voice_client.pause()
        else:
            await send_command_error_message(ctx, 'Currently there isn\'t a played song to pause.')

    @commands.command()
    async def resume(self, ctx):
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if bot_voice_client and bot_voice_client.is_paused():
            bot_voice_client.resume()
        else:
            await send_command_error_message(ctx, 'Currently there isn\'t a paused song to resume.')

    @commands.command()
    async def stop(self, ctx):
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if bot_voice_client and bot_voice_client.is_playing():
            bot_voice_client.stop()
        else:
            await send_command_error_message(ctx, 'Currently there isn\'t a played song to stop.')

    #@commands.command(aliases=['n'])
    #async def next(self, ctx):

    @commands.command()
    async def clear(self, ctx):
        await self.stop(ctx)

        self.__song_queue = []
        self.__song_details = {}

    @commands.command()
    async def queue(self, ctx):
        i = 0
        for details in self.__song_details.values():
            description = f'{i + 1}. {details["title"]}\n'

        await ctx.send(embed=discord.Embed(
            title=f'{self.__bot.user.name} queue',
            description=description,
            colour=discord.Colour.blue()))


def setup(bot):
    bot.add_cog(music_operations(bot))
