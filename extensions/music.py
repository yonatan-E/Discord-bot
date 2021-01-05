import discord
from discord.ext import commands
from discord.utils import get

from util.error_handling import create_error_embed
from util.music_queue import music_queue
from util.music_util import yt_searcher

class music(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot

        self.__server_queues = {}
        self.__yt_searcher = yt_searcher()
    
    def play_next(self, voice_client):
        song_queue = self.__server_queues[voice_client.guild.id]
        
        try:
            voice_client.play(discord.FFmpegPCMAudio(song_queue.url), after=lambda e: self.play_next(voice_client))
        except:
            pass

        if song_queue.index in range(0, len(song_queue)):
            song_queue.index += 1
        else:
            song_queue.index = 0

    @commands.command(aliases=['PLAY', 'p', 'P'], help='Add a song to the queue and/or play the next song from the queue.\nUsage: **$play <song_name>** or **$play**')
    async def play(self, ctx, *, name):
        if not await ctx.invoke(self.__bot.get_command('join')):
            return

        if ctx.guild.id not in self.__server_queues:
            self.__server_queues[ctx.guild.id] = music_queue()
        song_queue = self.__server_queues[ctx.guild.id]

        title, url = self.__yt_searcher.search(name)

        if title not in song_queue:
            song_queue[title] = url

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)
        
        if bot_voice_client.is_playing() or bot_voice_client.is_paused():
            await ctx.send(embed=discord.Embed(
                title=f'Queued {title}',
                colour=discord.Colour.blue()))
        else:
            await ctx.send(embed=discord.Embed(
                title=f'Playing {title}',
                colour=discord.Colour.blue()))
            
            song_queue.index = list.index(song_queue, title)
            self.play_next(bot_voice_client)

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            if not await ctx.invoke(self.__bot.get_command('join')):
                return

            if ctx.guild.id not in self.__server_queues:
                self.__server_queues[ctx.guild.id] = music_queue()
            song_queue = self.__server_queues[ctx.guild.id]

            if not song_queue:
                await ctx.send(create_error_embed(f'{self.__bot.user.name} queue is empty.'))

            else:
                bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

                if bot_voice_client.is_paused():
                    bot_voice_client.resume()
                
                elif not bot_voice_client.is_playing():
                    await ctx.send(embed=discord.Embed(
                        title=f'Playing {song_queue.title}',
                        colour=discord.Colour.blue()))

                    self.play_next(bot_voice_client)

    @commands.command(aliases=['PAUSE'], help='Pause the played song.\nUsage: **$pause**')
    async def pause(self, ctx):
        if not ctx.author.voice:
            await send_command_error_message(ctx, 'You have to connect to voice channel before you can do this command.')
            return

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await ctx.send(create_error_embed(f'{self.__bot.user.name} is not connected to a voice channel.'))
        elif not bot_voice_client.is_playing():
            await ctx.send(create_error_embed('Currently there isn\'t a played song to pause.'))
        else:
            bot_voice_client.pause()

    @commands.command(aliases=['RESUME'], help='Resume the paused song.\nUsage: **$resume**')
    async def resume(self, ctx):
        if not ctx.author.voice:
            await ctx.send(create_error_embed('You have to connect to voice channel before you can do this command.'))
            return

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await ctx.send(create_error_embed(f'{self.__bot.user.name} is not connected to a voice channel.'))
        elif not bot_voice_client.is_paused():
            await ctx.send(create_error_embed('Currently there isn\'t a paused song to resume.'))
        else:
            bot_voice_client.resume()

    @commands.command(aliases=['NEXT', 'n', 'N'], help='Play the next song from the queue.\nUsage: **$next**')
    async def next(self, ctx):
        if not ctx.author.voice:
            await ctx.send(create_error_embed('You have to connect to voice channel before you can do this command.'))
            return

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await ctx.send(create_error_embed(f'{self.__bot.user.name} is not connected to a voice channel.'))

        elif bot_voice_client.is_connected():
            song_queue = self.__server_queues[ctx.guild.id]

            if not song_queue.index in range(0, len(song_queue)):
                await ctx.send(create_error_embed('There isn\'t a next song.'))
            else:
                await ctx.send(embed=discord.Embed(
                    title=f'Playing {song_queue.title}',
                    colour=discord.Colour.blue()))
                
                bot_voice_client.stop()

    @commands.command(aliases=['PREV'], help='Play the prev song from the queue.\nUsage: **$prev**')
    async def prev(self, ctx):
        if not ctx.author.voice:
            await ctx.send(create_error_embed('You have to connect to voice channel before you can do this command.'))
            return

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await ctx.send(create_error_embed(f'{self.__bot.user.name} is not connected to a voice channel.'))

        elif bot_voice_client.is_connected():
            song_queue = self.__server_queues[ctx.guild.id]

            if not song_queue.index - 2 in range(0, len(song_queue)):
                await ctx.send(create_error_embed('There isn\'t a prev song.'))
            else:
                song_queue.index -= 2
                await ctx.send(embed=discord.Embed(
                    title=f'Playing {song_queue.title}',
                    colour=discord.Colour.blue()))
                
                bot_voice_client.stop()

    @commands.command(aliases=['JUMP'], help='Play the song in the specified place in the queue.\nUsage: **$jump <place_in_queue>** or **$jump**')
    async def jump(self, ctx, place: int):
        if not ctx.author.voice:
            await ctx.send(create_error_embed('You have to connect to voice channel before you can do this command.'))
            return

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await ctx.send(create_error_embed(f'{self.__bot.user.name} is not connected to a voice channel.'))

        elif bot_voice_client.is_connected():
            song_queue = self.__server_queues[ctx.guild.id]

            if not place - 1 in range(0, len(song_queue)):
                await ctx.send(create_error_embed('There specified place is not in the queue.'))
            else:
                song_queue.index = place - 1
                await ctx.send(embed=discord.Embed(
                    title=f'Playing {song_queue.title}',
                    colour=discord.Colour.blue()))
                
                bot_voice_client.stop()

    @jump.error
    async def jump_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(create_error_embed('Please enter a valid number.'))
        
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await self.jump(ctx, len(self.__server_queues[ctx.guild.id]))

    @commands.command(aliases=['STOP'], help='Stop the queue.\nUsage: **$stop**')
    async def stop(self, ctx):
        if not ctx.author.voice:
            await ctx.send(create_error_embed('You have to connect to voice channel before you can do this command.'))
            return

        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if not bot_voice_client:
            await ctx.send(create_error_embed(f'{self.__bot.user.name} is not connected to a voice channel.'))
        
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
        if ctx.guild.id not in self.__server_queues or not self.__server_queues[ctx.guild.id]:
            description = 'The queue is empty right now.'
        
        else:
            song_queue = self.__server_queues[ctx.guild.id]
            bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

            description = ''
            for i in range(0, len(song_queue)):
                description += f'**{i + 1}.** {song_queue[i]}'
                if i == song_queue.index - 1 and bot_voice_client and (bot_voice_client.is_playing() or bot_voice_client.is_paused()):
                    description += ' - **current**'
                description += '\n'

        await ctx.send(embed=discord.Embed(
            title=f'{self.__bot.user.name} queue',
            description=description,
            colour=discord.Colour.blue()))


def setup(bot):
    bot.add_cog(music(bot))