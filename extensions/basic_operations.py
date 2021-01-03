import discord
from discord.ext import commands

from util.error_handling import send_command_error_message

class basic_operations(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot

    #@commands.Cog.listener()
    #async def on_ready(self):
        #await self.__bot.change_presence(activity=discord.Game('JontiBot'))

    #    for guild in self.__bot.guilds:
    #        for channel in guild.channels:
    #            if isinstance(channel, discord.TextChannel):
    #                await channel.send(embed=discord.Embed(
    #                    title=f'{self.__bot.user.name} is working <:beers:795025887737020436>',
    #                    colour=discord.Colour.blue()))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.send(embed=discord.Embed(
                    title=f'Welcome {member.name} <:beers:795025887737020436>',
                    colour=discord.Colour.blue()))

    @commands.Cog.listener()
    async def on_server_join(self, guild):
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.send(embed=discord.Embed(
                    title=f'I\'m ready <:beers:795025887737020436>',
                    colour=discord.Colour.blue()))

    @commands.command(help='Delete the last messages from the chat.\nUsage: **$delete <number_of_messages>**')
    async def delete(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await send_command_error_message(ctx, 'Please enter a valid number.')
        else:
            await send_command_error_message(ctx, str(error))

    @commands.command(aliases=['INFO'], help='Get info about the bot.\nUsage: **$info**')
    async def info(self, ctx):
        await ctx.send(embed=discord.Embed(
            title=f'{self.__bot.user.name} info',
            description=f'The bot version is {self.__bot.VERSION}.\nThe bot was developed by JONTI.',
            colour=discord.Colour.blue()))

    @commands.command(aliases=['HELP'], help='Get right here.\nUsage: **$help**')
    async def help(self, ctx):
        embed = discord.Embed(
            title=f'{self.__bot.user.name} help',
            colour=discord.Colour.blue())

        for command in self.__bot.commands:
            embed.add_field(name=command, value=command.help, inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(basic_operations(bot))