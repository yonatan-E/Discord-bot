import discord
from discord.ext import commands

class basic_operations(commands.Cog):

    def __init__(self, bot):
        self.__bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.__bot.change_presence(activity=discord.Game('JontiBot'))

        for guild in self.__bot.guilds:
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    await channel.send(embed=discord.Embed(
                        title=f'{self.__bot.user.name} is working <:handshake:794249925248417802>',
                        colour=discord.Colour.blue()))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send(f'Welcome, {member.mention}!')

    @commands.Cog.listener()
    async def on_server_join(self, guild):
        await guild.owner.send(f'Im ready!')

    @commands.command(help='Clear the last messages from the chat.\nUsage: $clear <number_of_messages>')
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(embed=discord.Embed(
                title='Couldn\'t complete clear command',
                description=f'{error.arguments} is not a number!',
                colour=discord.Colour.red()))

    @commands.command(help='Get info about the bot.')
    async def info(self, ctx):
        await ctx.send(embed=discord.Embed(
            title=f'{self.__bot.user.name} info',
            description=f'The bot version is {self.__bot.VERSION}.\nThe bot was developed by JONTI.',
            colour=discord.Colour.blue()))

    @commands.command(help='Get right here.')
    async def help(self, ctx):
        embed = discord.Embed(
            title=f'{self.__bot.user.name} help',
            colour=discord.Colour.blue())

        for command in self.__bot.commands:
            embed.add_field(name=command, value=command.help, inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(basic_operations(bot))