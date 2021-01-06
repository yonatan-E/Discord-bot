import util.tictactoe.player

class tictactoe:

	WINNING_STATES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

	def __init__(self, players):
		self.__board = [''] * 9

		self.__players = players
		self.__current_player = players[0]

	def do_turn(self, player, place):
		player.play_turn(self.__board, place)

	def is_winning(self, player):
		for state in self.WINNING_STATES:
			if len([place for place in state if self.__board[place] == player.symbol]) == len(state):
				return True
		return False

	def switch_player(self):
		self.__current_player = self.__players[(self.__players.index(self.__current_player) + 1) % len(self.__players)]

	@property
	def board(self):
		return self.__board

	@property
	def players(self):
		return self.__players

	@property
	def current_player(self):
		return self.__current_player