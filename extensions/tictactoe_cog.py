import discord
from discord.ext import commands

from discord.utils import get

from util.error_handling import create_error_embed

from util.tictactoe.tictactoe_wrapper import tictactoe_wrapper
from util.tictactoe.tictactoe_board import tictactoe_board
from util.tictactoe.player import player, ai_player
from util.tictactoe.discord_player import discord_player

class tictactoe_cog(commands.Cog):

	qualified_name = 'tictactoe'
	description = 'The commands of the tictactoe game of the bot.'

	def __init__(self, bot):
		self.__bot = bot

		self.__server_tictactoes = {}

		self.__symbols = {'': ':white_medium_square:', 'x': ':regional_indicator_x:', 'o': ':regional_indicator_o:'}

	def create_board_message(self, board):
		from math import sqrt

		board_size = len(board)
		board_length = sqrt(board_size)

		custom_board = ''
		for i in range(1, board_size + 1):
			custom_board += self.__symbols[board[i]]

			if i % board_length == 0:
				custom_board += '\n'

		return custom_board

	@commands.command(aliases=['TICTACTOE'], help='Start a tictactoe game.')
	async def tictactoe(self, ctx, member: discord.Member):
		if not ctx.guild.id in self.__server_tictactoes:
			self.__server_tictactoes[ctx.guild.id] = []

		current_games = self.__server_tictactoes[ctx.guild.id]

		if [game for game in current_games if ctx.author.id in [player.discord_id for player in game.players]]:
			await ctx.send(embed=create_error_embed(f'{ctx.author.name}, you are already in a tictactoe game.'))
			return
		
		if [game for game in current_games if member.id in [player.discord_id for player in game.players]]:
			await ctx.send(embed=create_error_embed(f'{member.name} is already in a tictactoe game.'))
			return
		
		game = tictactoe_wrapper(tictactoe_board(), [discord_player(player('x'), ctx.author), discord_player(player('o'), member)])
		current_games.append(game)
		
		await ctx.send(self.create_board_message(game.board))
		await ctx.send(embed=discord.Embed(
            title=f'{game.players[0].discord_name} vs {game.players[1].discord_name}',
            description=f'{game.current_player.discord_name}\'s turn.',
            colour=discord.Colour.blue()))

	@tictactoe.error
	async def tictactoe_error(self, ctx, error):
		if isinstance(error, commands.errors.MissingRequiredArgument):
			await self.tictactoe(ctx, self.__bot.user)
		elif isinstance(error, commands.errors.MemberNotFound):
			await ctx.send(embed=create_error_embed(str(error)))

	@commands.command(aliases=['PLACE'], help='Place a player symbol in a tictactoe game board.')
	async def place(self, ctx, place: int):
		try:
			current_games = self.__server_tictactoes[ctx.guild.id]
			game = [game for game in current_games if ctx.author.id in [player.discord_id for player in game.players]][0]
		except:
			await ctx.send(embed=create_error_embed(f'{ctx.author.name}, you have to be in a tictactoe game to do this command.'))
			return

		if ctx.author.id != game.current_player.discord_id:
			await ctx.send(embed=create_error_embed(f'{ctx.author.name}, it is not your turn.'))
			return

		try:
			game.do_turn(place)
		except IndexError as e:
			await ctx.send(embed=create_error_embed(f'{e} Please enter another place.'))
			return

		await ctx.send(self.create_board_message(game.board))

		if game.is_winning():
			await ctx.send(embed=discord.Embed(
	            title=f'{game.current_player.discord_name} won <:beers:795025887737020436>',
	            colour=discord.Colour.blue()))

			current_games.remove(game)
			return

		elif game.board.is_full():
			await ctx.send(embed=discord.Embed(
	            title='Draw <:beers:795025887737020436>',
	            colour=discord.Colour.blue()))

			current_games.remove(game)
			return

		game.switch_player()
		await ctx.send(embed=discord.Embed(
            title=f'{game.players[0].discord_name} vs {game.players[1].discord_name}',
            description=f'{game.current_player.discord_name}\'s turn.',
            colour=discord.Colour.blue()))

	@place.error
	async def place_error(self, ctx, error):
		if isinstance(error, commands.errors.BadArgument):
			await ctx.send(embed=create_error_embed('Please enter a valid number.'))

	@commands.command(name='tictactoe-end', aliases=['TICTACTOE-END'], help='End a tictactoe game.')
	async def tictactoe_end(self, ctx):
		try:
			current_games = self.__server_tictactoes[ctx.guild.id]

			game = list(filter(lambda game: ctx.author.id in [player.discord_id for player in game.players], current_games))[0]
			current_games.remove(game)
		except:
			await ctx.send(embed=create_error_embed(f'{ctx.author.name}, you have to be in a tictactoe game to do this command.'))
			return

		await ctx.send(embed=discord.Embed(
            title=f'{game.players[0].discord_name} vs {game.players[1].discord_name}',
            description=f'{ctx.author.name} ended the game.',
            colour=discord.Colour.blue()))



def setup(bot):
	bot.add_cog(tictactoe_cog(bot))