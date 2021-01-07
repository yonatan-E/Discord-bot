import discord
from discord.ext import commands

from util.error_handling import create_error_embed

class basic_cog(commands.Cog):

    qualified_name = 'basic'
    description = 'The basic commands of the bot.'

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

    @commands.command(help='Delete the last messages from the chat.')
    async def delete(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(embed=create_error_embed('Please enter a valid number.'))

    @commands.command(aliases=['INFO'], help='Get info about the bot.')
    async def info(self, ctx):
        await ctx.send(embed=discord.Embed(
            title=f'{self.__bot.user.name} info',
            description=f'**The bot version is {self.__bot.VERSION}.\nThe bot was developed by Yonatan Ehrenreich.**',
            colour=discord.Colour.blue()))

    @commands.command(aliases=['HELP'], help='Get right here.')
    async def help(self, ctx, *, category):
        cog = [cog for cog in self.__bot.cogs.values() if cog.qualified_name == category][0]

        embed = discord.Embed(
            title=f'{self.__bot.user.name} help',
            colour=discord.Colour.blue())

        embed.add_field(name=cog.qualified_name, value=f'**{cog.description}**', inline=False)

        for command in cog.walk_commands():
            embed.add_field(name=command, value=command.help, inline=False)

        await ctx.send(embed=embed)

    @help.error
    async def help_error(self, ctx, error):
        embed = discord.Embed(
            title=f'{self.__bot.user.name} help',
            description='**Please choose a category from the following categories:**',
            colour=discord.Colour.blue())

        for cog in self.__bot.cogs.values():
            embed.add_field(name=cog.qualified_name, value=f'{cog.description}', inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(basic_cog(bot))