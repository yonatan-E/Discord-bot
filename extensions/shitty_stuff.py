import discord
from discord.ext import commands

from discord.utils import get

class other_shit(commands.Cog):

	def __init__(self, bot):
		self.__bot = bot

	@commands.command()
	async def raz(self, ctx):
		voice_client = get(self.__bot.voice_clients, guild=ctx.guild)
		voice_client.play(discord.FFmpegPCMAudio('RAZ_x_TAL.WAV_x_WS_-_RUNNERS_98BPM.mp3'))

def setup(bot):
	bot.add_cog(other_shit(bot))