import discord
from discord.ext import commands


class music_operations(commands.Cog):
    def __init__(self, bot):
        self.__bot = bot

    @commands.command(aliases=['connect'], help='Make the bot to join to the current voice channel.')
    async def join(self, ctx):
        voice_client = ctx.author.voice

        if voice_client is None:
            await ctx.send(embed=discord.Embed(
                title='Couldn\'t complete join command',
                description=f'Please connect to a voice channel before joining {self.__bot.user.name} <:man_facepalming:794333151434113024>',
                colour=discord.Colour.red()))
            return

        elif [vc for vc in self.__bot.voice_clients if vc.guild == ctx.guild] != []:
            await ctx.send(embed=discord.Embed(
                title='Couldn\'t complete join command',
                description=f'{self.__bot.user.name} is already connected to another voice channel <:man_facepalming:794333151434113024>',
                colour=discord.Colour.red()))
            return

        await voice_client.channel.connect()

    @commands.command(aliases=['disconnect'], help='Make the bot to leave the current voice channel.')
    async def leave(self, ctx):
        for voice_client in self.__bot.voice_clients:
            if voice_client.guild == ctx.guild:
                await voice_client.disconnect()
                return

        await ctx.send(embed=discord.Embed(
            title='Couldn\'t complete leave command',
            description=f'Please join {self.__bot.user.name} to a voice channel before making it leave one <:man_facepalming:794333151434113024>',
            colour=discord.Colour.red()))

    

def setup(bot):
    bot.add_cog(music_operations(bot))
