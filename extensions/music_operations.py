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

        self.__server_queues = {}
        self.__yt_searcher = yt_searcher()

    @commands.command(aliases=['JOIN', 'connect', 'CONNECT'], help='Make the bot to join to the current voice channel. Usage: **$join**')
    async def join(self, ctx):
        member_voice_status = ctx.author.voice

        if not member_voice_status:
            await send_command_error_message(ctx, 'You have to connect to voice channel before you can do this command.')

        else:
            bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

            if bot_voice_client and bot_voice_client.channel.id != member_voice_status.channel.id:
                await send_command_error_message(ctx, f'{self.__bot.user.name} is already connected to another voice channel.')
            else:
                try:
                    await member_voice_status.channel.connect()
                except:
                    pass

                if ctx.guild.id not in self.__server_queues:
                    self.__server_queues[ctx.guild.id] = music_queue()
                else:
                    self.__server_queues[ctx.guild.id].index = 0

    @commands.command(aliases=['LEAVE', 'disconnect', 'DISCONNECT'], help='Make the bot to leave the current voice channel.\nUsage: **$leave**')
    async def leave(self, ctx):
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if bot_voice_client:
            await bot_voice_client.disconnect()
        else:
            await send_command_error_message(ctx, f'Please join {self.__bot.user.name} to a voice channel before making it leave one.')
    
    def play_next(self, voice_client):
        song_queue = self.__server_queues[voice_client.guild.id]
        
        try:
            voice_client.play(discord.FFmpegPCMAudio(song_queue.url), after=lambda e: self.play_next(voice_client))
        except:
            pass

        song_queue.index += 1

    @commands.command(aliases=['PLAY', 'p', 'P'], help='Add a song to the queue and/or play the next song from the queue.\nUsage: **$play <song_name>** or **$play**')
    async def play(self, ctx, *, name):
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)
    
        if not bot_voice_client:
            await self.join(ctx)
            bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

            if not bot_voice_client:
                return
    
        title, url = self.__yt_searcher.search(name)

        song_queue = self.__server_queues[ctx.guild.id]

        if title not in song_queue:
            song_queue[title] = url
    
        if not bot_voice_client.is_playing():
            self.play_next(bot_voice_client)

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

            if not bot_voice_client:
                await self.join(ctx)
                bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

                if not bot_voice_client:
                    return
            
            if bot_voice_client.is_paused():
                bot_voice_client.resume()
            elif not bot_voice_client.is_playing():
                self.play_next(bot_voice_client)

    @commands.command(aliases=['PAUSE'], help='Pause the played song.\nUsage: **$pause**')
    async def pause(self, ctx):
        if not ctx.author.voice:
            await send_command_error_message(ctx, 'You have to connect to voice channel before you can do this command.')
            return

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await send_command_error_message(ctx, f'{self.__bot.user.name} is not connected to a voice channel.')
        elif not bot_voice_client.is_playing():
            await send_command_error_message(ctx, 'Currently there isn\'t a played song to pause.')
        else:
            bot_voice_client.pause()

    @commands.command(aliases=['RESUME'], help='Resume the paused song.\nUsage: **$resume**')
    async def resume(self, ctx):
        if not ctx.author.voice:
            await send_command_error_message(ctx, 'You have to connect to voice channel before you can do this command.')
            return

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await send_command_error_message(ctx, f'{self.__bot.user.name} is not connected to a voice channel.')
        elif not bot_voice_client.is_paused():
            await send_command_error_message(ctx, 'Currently there isn\'t a paused song to resume.')
        else:
            bot_voice_client.resume()

    @commands.command(aliases=['NEXT', 'n', 'N'], help='Play the next song from the queue.\nUsage: **$next**')
    async def next(self, ctx):
        if not ctx.author.voice:
            await send_command_error_message(ctx, 'You have to connect to voice channel before you can do this command.')
            return

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await send_command_error_message(ctx, f'{self.__bot.user.name} is not connected to a voice channel.')

        elif bot_voice_client.is_connected():
            song_queue = self.__server_queues[ctx.guild.id]

            if not song_queue.index in range(0, len(song_queue)):
                await send_command_error_message(ctx, 'There isn\'t a next song.')
            else:
                bot_voice_client.stop()

    @commands.command(aliases=['PREV'], help='Play the prev song from the queue.\nUsage: **$prev**')
    async def prev(self, ctx):
        if not ctx.author.voice:
            await send_command_error_message(ctx, 'You have to connect to voice channel before you can do this command.')
            return

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await send_command_error_message(ctx, f'{self.__bot.user.name} is not connected to a voice channel.')

        elif bot_voice_client.is_connected():
            song_queue = self.__server_queues[ctx.guild.id]

            if not song_queue.index - 2 in range(0, len(song_queue)):
                await send_command_error_message(ctx, 'There isn\'t a prev song.')
            else:
                song_queue.index -= 2
                bot_voice_client.stop()

    @commands.command(aliases=['JUMP'], help='Play the song in the specified place in the queue.\nUsage: **$jump <place_in_queue>** or **$jump**')
    async def jump(self, ctx, place: int):
        if not ctx.author.voice:
            await send_command_error_message(ctx, 'You have to connect to voice channel before you can do this command.')
            return

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await send_command_error_message(ctx, f'{self.__bot.user.name} is not connected to a voice channel.')

        elif bot_voice_client.is_connected():
            song_queue = self.__server_queues[ctx.guild.id]

            if not place in range(0, len(song_queue)):
                await send_command_error_message(ctx, 'There specified place is not in the queue.')
            else:
                song_queue.index = place
                bot_voice_client.stop()

    @jump.error
    async def jump_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await send_command_error_message(ctx, 'Please enter a valid number.')
        
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            song_queue.index = len(self.__server_queues[ctx.guild.id]) - 1
            bot_voice_client.stop()

    @commands.command(aliases=['STOP'], help='Stop the queue.\nUsage: **$stop**')
    async def stop(self, ctx):
        if not ctx.author.voice:
            await send_command_error_message(ctx, 'You have to connect to voice channel before you can do this command.')
            return

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await send_command_error_message(ctx, f'{self.__bot.user.name} is not connected to a voice channel.')
        
        elif bot_voice_client.is_connected():
            song_queue = self.__server_queues[ctx.guild.id]
            song_queue.index = -1

            bot_voice_client.stop()

    @commands.command(aliases=['CLEAR'], help='Clear the queue\nUsage: **$clear**')
    async def clear(self, ctx):
        await self.stop(ctx)

        self.__server_queues[ctx.guild.id] = music_queue()

    @commands.command(aliases=['QUEUE'], help='Show the queue.\nUsage: **$queue**')
    async def queue(self, ctx):
        song_queue = self.__server_queues[ctx.guild.id]
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        description = ''
        for i in range(0, len(song_queue)):
            description += f'**{i + 1}.** {song_queue[i]}'
            if i == song_queue.index - 1 and bot_voice_client and bot_voice_client.is_connected():
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
