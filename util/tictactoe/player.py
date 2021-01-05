class player:

	def __init__(self, symbol):
		self.__symbol = symbol

	def play_turn(self, board, place):
		if place - 1 not in range(0, 9):
			raise IndexError(f'Place {place} is not in range.')
		elif self.__board[place - 1]:
			raise IndexError(f'Place {place} is already taken.')

		board[place - 1] = self.__symbol

	@property
	def symbol(self):
		return self.__symbol

class ai_player(player):

	def play_turn(self, board, place):
		if place - 1 not in range(0, 9):
			raise IndexError(f'Place {place} is not in range.')
		elif self.__board[place - 1]:
			raise IndexError(f'Place {place} is already taken.')

		board[place - 1] = self.__symbol