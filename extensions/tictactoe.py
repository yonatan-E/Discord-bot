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

		if list(filter(lambda game: ctx.author.id in [player.discord_id for player in game.players], current_games)):
			await send_command_error_message(f'You are already in a tictactoe game.')
			return

		if list(filter(lambda game: member.id in [player.discord_id for player in game.players], current_games)):
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

	@commands.command(aliases=['PLACE'])
	async def place(self, ctx, place: int):
		current_games = self.__server_tictactoes[ctx.guild.id]

		try:
			game = len(filter(lambda game: ctx.author.id in [player.discord_id for player in game.players], current_games))[0]
		except:
			await send_command_error_message(ctx, f'{ctx.member.name}, you have to be in a tictactoe game to do this command.')
			return

		if ctx.author.id != game.current_player.id:
			await send_command_error_message(ctx, f'{ctx.member.name}, it is not your turn.')
			return

		try:
			game.do_turn(place)
		except IndexError as e:
			await send_command_error_message(ctx, f'{e} Please enter another place.')
			return

		if game.is_winning():
			await ctx.send(embed=discord.Embed(
	            title=f'{game.current_player.discord_name} won.',
	            colour=discord.Colour.blue()))

			current_games.remove(game)
			return

		game.switch_player()

	@place.error
	async def place_error(self, ctx, error):
		if isinstance(error, commands.errors.BadArgument):
            await send_command_error_message(ctx, 'Please enter a valid number.')


def setup(bot):
	bot.add_cog(tictactoe(bot))