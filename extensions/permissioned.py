import discord
from discord.ext import commands

from util.error_handling import create_error_embed

class permissioned(commands.Cog):

    qualified_name = 'permissioned'
    description = 'The permissioned commands of the bot. You need to get a permission to do these commands.'

    def __init__(self, bot):
        self.__bot = bot

        permissioned.cog_command_error = lambda self, ctx, error: ctx.send(embed=create_error_embed(str(error)))

    @commands.command(aliases=['KICK'], help='Kick a member from the server.')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason='no reason'):
        if ctx.author.id == member.id:
            await ctx.send(f'{member.name}, you can\'t kick yourself.')
            return

        await ctx.guild.kick(user=member, reason=reason)
        await ctx.send(embed=discord.Embed(
            title=f'Member {member.name} was kicked because of {reason}.',
            colour=discord.Colour.red()))

    @commands.command(aliases=['BAN'], help='Ban a member from the server.')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason='no reason'):
        if ctx.author.id == member.id:
            await ctx.send(embed=discord.Embed(
                title=f'{member.name}, you can\'t ban yourself.',
                colour=discord.Colour.red()))
            return

        await ctx.guild.ban(user=member, reason=reason)
        await ctx.send(embed=discord.Embed(
            title=f'Member {member.name} was banned because of {reason}.',
            colour=discord.Colour.red()))
    
    @commands.command(aliases=['UNBAN'], help='Unban a member from the server.')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(embed=discord.Embed(
                    title=f'Member {user.name} was unbanned',
                    colour=discord.Colour.blue()))
                return

        raise commands.errors.MemberNotFound(member)


def setup(bot):
    bot.add_cog(permissioned(bot))