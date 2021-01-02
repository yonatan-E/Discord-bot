import discord
from discord.ext import commands
from discord.utils import get

import youtube_dl

from util.error_handling import send_command_error_message
from util.music_queue import music_queue
from util.music_util import yt_searcher

class music_operations(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot

        self.__song_queue = music_queue()
        self.__yt_searcher = yt_searcher()

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

                self.__song_queue.reset()

    @commands.command(aliases=['disconnect'], help='Make the bot to leave the current voice channel.')
    async def leave(self, ctx):
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if bot_voice_client:
            await bot_voice_client.disconnect()
        else:
            await send_command_error_message(ctx, f'Please join {self.__bot.user.name} to a voice channel before making it leave one.')
    
    def play_next(self, voice_client):
        try:
            title, url = self.__song_queue.next()
            voice_client.play(discord.FFmpegPCMAudio(url), after=lambda e: self.play_next(voice_client))

            await channel.send(embed=discord.Embed(
                title=f'Playing {title}',
                colour=discord.Colour.blue()))
            
        except IndexError:
            pass

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, name):
        title, url = self.__yt_searcher.search(name)

        if title not in self.__song_queue:
            self.__song_queue[title] = url
        
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await self.join(ctx)
            bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)
        
        if bot_voice_client.is_connected() and not bot_voice_client.is_playing():
            self.play_next(bot_voice_client)

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

            if not bot_voice_client:
                await self.join(ctx)
                bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)
            
            if bot_voice_client.is_connected():
                if bot_voice_client.is_paused():
                    bot_voice_client.resume()
                elif not bot_voice_client.is_playing():
                    self.play_next(bot_voice_client)

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

    @commands.command(aliases=['n'])
    async def next(self, ctx):
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await send_command_error_message(ctx, f'{self.__bot.user.name} is not connected to a voice channel.')
        if bot_voice_client.is_playing():
            bot_voice_client.stop()

        try:
            next_song_url = self.__song_queue.next()
            bot_voice_client.play(discord.FFmpegPCMAudio(next_song_url), after=lambda e: self.play_next(bot_voice_client))
        except IndexError:
            await send_command_error_message(ctx, 'There isn\'t a next song.')

    @commands.command()
    async def prev(self, ctx):
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await send_command_error_message(ctx, f'{self.__bot.user.name} is not connected to a voice channel.')
        if bot_voice_client.is_playing():
            bot_voice_client.stop()

        try:
            next_song_url = self.__song_queue.prev()
            bot_voice_client.play(discord.FFmpegPCMAudio(next_song_url), after=lambda e: self.play_next(bot_voice_client))
        except IndexError:
            await send_command_error_message(ctx, 'There isn\'t a prev song.')

    @commands.command()
    async def clear(self, ctx):
        await self.stop(ctx)

        self.__song_queue = music_queue()

    @commands.command()
    async def queue(self, ctx):
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        description = ''
        for i in range(0, len(self.__song_queue)):
            description += f'**{i + 1}.** {self.__song_queue[i]}'
            if i == self.__song_queue.current and bot_voice_client and bot_voice_client.is_connected():
                description += ' - **current**'
            description += '\n'

        if not description:
            description = 'The queue is empty right now.'

        await ctx.send(embed=discord.Embed(
            title=f'{self.__bot.user.name} queue',
            description=description,
            colour=discord.Colour.blue()))


def setup(bot):
    bot.add_cog(music_operations(bot))
