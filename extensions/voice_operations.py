import discord
from discord.ext import commands
from discord.utils import get

from util.error_handling import send_command_error_message

class voice_operations(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot

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

                return True

        return False

    @commands.command(aliases=['LEAVE', 'disconnect', 'DISCONNECT'], help='Make the bot to leave the current voice channel.\nUsage: **$leave**')
    async def leave(self, ctx):
        bot_voice_client = get(self.__bot.voice_clients, guild=ctx.guild)

        if bot_voice_client:
            await bot_voice_client.disconnect()
        else:
            await send_command_error_message(ctx, f'Please join {self.__bot.user.name} to a voice channel before making it leave one.')


def setup(bot):
    bot.add_cog(voice_operations(bot))