import discord
from discord.ext import commands

from discord.utils import get

from util.error_handling import send_command_error_message

from util.tictactoe.tictactoe import tictactoe as tictactoe_game
from util.tictactoe.player import player, ai_player
from util.tictactoe.discord_player import discord_player

class tictactoe(commands.Cog):

	def __init__(self, bot):
		self.__bot = bot

		self.__server_tictactoes = {}

		self.__symbols = {'': ':black_square_button:', 'x': ':regional_indicator_x:', 'o': ':regional_indicator_o:'}

	def create_custom_board(self, tictactoe):
		from math import sqrt

		board_size = len(tictactoe.board)
		board_length = sqrt(board_size)

		custom_board = ''
		for i in range(0, board_size):
			custom_board += self.__symbols[tictactoe.board[i]]

			if (i + 1) % board_length == 0:
				custom_board += '\n'

		return custom_board

	@commands.command(aliases=['TICTACTOE'])
	async def tictactoe(self, ctx, member: discord.Member):
		if not ctx.guild.id in self.__server_tictactoes:
			self.__server_tictactoes[ctx.guild.id] = []

		current_games = self.__server_tictactoes[ctx.guild.id]

		if ctx.author.id in [player.discord_id for player in [game.players for game in current_games]]:
			await send_command_error_message(f'{member.name} is already in a tictactoe game.')
			return

		game = tictactoe_game(discord_player(player('x'), ctx.author), discord_player(player('o'), member))
		current_games.append(game)

		await ctx.send(self.create_custom_board(game))
		await ctx.send(embed=discord.Embed(
            title=f'{game.current_player.discord_name}\'s turn.',
            colour=discord.Colour.blue()))

	@tictactoe.error
	async def tictactoe_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingRequiredArgument):
			await self.tictactoe(ctx, self.__bot.user)
		elif isinstance(error, commands.errors.BadArgument):
			await send_command_error_message(ctx, 'Please enter a valid user name.')
		else:
			await send_command_error_message(ctx, str(error))

	@commands.command(aliases=['PLACE'])
	async def place(self, ctx, place: int):



def setup(bot):
	bot.add_cog(tictactoe(bot))