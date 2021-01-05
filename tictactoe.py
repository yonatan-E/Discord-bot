class tictactoe:

	WINNING_STATES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

	def __init__(self, player1, player2):
		self.__board = [None] * 9

		self.__players = [player1, player2]
		self.__current_player = player1

	def do_turn(self, place):
		self.__current_player.play_turn(self.__board, place)

	def switch_player(self):
		self.__current_player = self.__players[(self.__players.index(self.__current_player) + 1) % len(self.__players)]

	def is_winning(self):
		for state in WINNING_STATES:
			if self.__board[state[0]] == self.__current_player.symbol and self.__board[state[1]] == self.__current_player.symbol 
				and self.__board[state[2]] == self.__current_player.symbol:
				return True
		return False

	@property
	def players(self):
		return self.__players

class player:

	def __init__(self, symbol):
		self.__symbol = symbol

	@property
	def symbol(self):
		return self.__symbol

class human_player(player):

	def play_turn(self, board, place):
		if place - 1 not in range(0, 9):
			raise IndexError(f'Place {place} is not in range')
		elif self.__board[place - 1]:
			raise IndexError(f'Place {place} is already taken.')

		board[place - 1] = self.__symbol

class ai_player(player):

	def play_turn(self, board, place):
		if place - 1 not in range(0, 9):
			raise IndexError(f'Place {place} is not in range')
		elif self.__board[place - 1]:
			raise IndexError(f'Place {place} is already taken.')

		board[place - 1] = self.__symbol

class board:

	def __init__(self, ):
		self.__board = ['', '', '', '', '', '', '', '', '']

	def __setitem__(self, index, ):