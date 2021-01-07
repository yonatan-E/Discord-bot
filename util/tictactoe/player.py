class player:

	def __init__(self, symbol):
		self.__symbol = symbol

	def play_turn(self, board, place):
		board[place] = self.__symbol

	@property
	def symbol(self):
		return self.__symbol

class ai_player(player):

	def play_turn(self, board, place):
		board[place] = self.__symbol