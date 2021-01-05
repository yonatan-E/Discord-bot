import discord

import util.tictactoe.player

class discord_player:

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