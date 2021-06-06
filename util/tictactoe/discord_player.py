import discord

from util.tictactoe.player import player

class discord_player(player):

	def __init__(self, player, member):
		self.__player = player
		self.__member = member

	def play_turn(self, board, place):
		self.__player.play_turn(board, place)

	@property
	def symbol(self):
		return self.__player.symbol

	@property
	def discord_id(self):
		return self.__member.id

	@property
	def discord_name(self):
		return self.__member.name
